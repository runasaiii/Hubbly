# Python modules
from typing import Any

# Django modules
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView

# DRF modules
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

# Project modules
from .models import CustomUser, Profile
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
    UserLoginSerializer,
    RegistrationSerializer,
    UserWithProfileSerializer,
    UserLoginErrorsSerializer,
    HTTP405MethodNotAllowedSerializer,
    RegistrationErrorsSerializer,
    ProfileUpdateErrorsSerializer,
    UserNotFoundSerializer,
)

# Swagger modules
from drf_spectacular.utils import extend_schema, OpenApiResponse


def user_list(request):
    """
    User list controller
    """
    users: CustomUser = CustomUser.objects.all()
    serializer: UserSerializer = UserSerializer(
        to=users,
        many=True
        )
    return JsonResponse(
        serializer.data,
        safe=False)


def user_detail(request, user_id):
    """
    User detail controller
    """
    try:
        user: CustomUser = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=404)
    serializer: UserSerializer = UserSerializer(user)
    return JsonResponse(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain pair view using CustomTokenObtainPairSerializer
    """
    serializer_class: CustomTokenObtainPairSerializer = CustomTokenObtainPairSerializer


class CustomUserViewSet(ViewSet):
    """ Creating login endpoints for custom user"""

    @extend_schema(
        summary="User Login",
        # description="My custom deprecation reason",
        request=UserLoginSerializer,
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successful login returns user data along with access and refresh tokens.",
                response=UserWithProfileSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request due to invalid input data.",
                response=UserLoginErrorsSerializer,
            ),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                description="Method not allowed. You used wrong HTTP request type. Only POST can be used to reach this endpoint.",
                response=HTTP405MethodNotAllowedSerializer,
            )
        }
    )
    @action(
        methods=('POST',),
        detail=False,
        url_path='login',
        url_name='login',
        permission_classes=(AllowAny,)
    )
    def login(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],

    ) -> DRFResponse:

        serializer: UserLoginSerializer = UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user: CustomUser = serializer.validated_data.pop("user")

        refresh_token: RefreshToken = RefreshToken.for_user(user)
        access_token: str = str(refresh_token.access_token)

        return DRFResponse(
            data={
                'id': user.id,
                'email': user.email,
                'access': access_token,
                'refresh': str(refresh_token),
            },
            status=HTTP_200_OK
        )

    @extend_schema(
        summary="User Registration",
        request=RegistrationSerializer,
        responses={
            HTTP_201_CREATED: OpenApiResponse(
                description="User successfully registered.",
                response=UserWithProfileSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid registration data.",
                response=RegistrationErrorsSerializer,
            ),
        }
    )
    @action(
        methods=('POST',),
        detail=False,
        url_path='register',
        url_name='register',
        permission_classes=(AllowAny,)
    )
    def register(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        serializer: RegistrationSerializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: CustomUser = serializer.save()

        refresh_token: RefreshToken = RefreshToken.for_user(user)
        access_token: str = str(refresh_token.access_token)

        return DRFResponse(
            data={
                'id': user.id,
                'email': user.email,
                'access': access_token,
                'refresh': str(refresh_token),
            },
            status=HTTP_200_OK
        )


    @extend_schema(
        summary="Get personal user data",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Return personal user data with profile information.",
                response=UserWithProfileSerializer,
            ),
            HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Authentication credentials were not provided or invalid.",
            ),
        }
    )
    @action(
        methods=('GET',),
        detail=False,
        url_path='personal_data',
        url_name='personal_data',
        permission_classes=(IsAuthenticated,),
    )
    def display_personal_data(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:

        user: CustomUser = request.user
        serializer = UserWithProfileSerializer(user)
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )


    @extend_schema(
        summary="Retrieve or update user profile",
        request=ProfileUpdateSerializer,  # используется только для PATCH
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Profile retrieved (GET) or updated (PATCH) successfully.",
                response=ProfileSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data for updating profile (PATCH).",
                response=ProfileUpdateErrorsSerializer,
            ),
            HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Authentication required.",
            ),
        }
    )
    @action(
        methods=('GET', 'PATCH'),
        detail=False,
        url_path='profile',
        url_name='profile',
        permission_classes=(IsAuthenticated,),
    )
    def profile(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        user: CustomUser = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
            return DRFResponse(
                data=serializer.data,
                status=HTTP_200_OK
            )

        elif request.method == 'PATCH':
            data = request.data.copy()

            if 'interests' in data and isinstance(data['interests'], str):
                import json
                try:
                    data['interests'] = json.loads(data['interests'])
                except json.JSONDecodeError:
                    data['interests'] = []

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            serializer = ProfileUpdateSerializer(
                instance=profile,
                data=data, 
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return DRFResponse(ProfileSerializer(profile).data, status=HTTP_200_OK)


    @extend_schema(
        summary="Upload user avatar",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Avatar uploaded successfully.",
                response=ProfileSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="No avatar file provided.",
            ),
            HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Authentication required.",
            ),
        }
    )
    @action(
        methods=('POST',),
        detail=False,
        url_path='profile/avatar',
        url_name='upload_avatar',
        permission_classes=(IsAuthenticated,),
    )
    def upload_avatar(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """Upload avatar for user profile."""
        user: CustomUser = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        if 'avatar' not in request.FILES:
            return DRFResponse(
                data={'error': 'No file provided'},
                status=HTTP_400_BAD_REQUEST
            )

        profile.avatar = request.FILES['avatar']
        profile.save()

        serializer = ProfileSerializer(profile)
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )


    @action(
        methods=('GET',),
        detail=True,
        url_path='profile',
        url_name='user_profile',
        permission_classes=(IsAuthenticated,),
    )
    def get_user_profile(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get profile of a specific user by user ID"""
        user_id = kwargs.get('pk')
        try:
            target_user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return DRFResponse(
                data={'error': 'User not found'},
                status=HTTP_404_NOT_FOUND
            )

        profile, created = Profile.objects.get_or_create(user=target_user)
        serializer = ProfileSerializer(profile)

        user_serializer = UserSerializer(target_user)

        return DRFResponse(
            data={
                'user': user_serializer.data,
                'profile': serializer.data
            },
            status=HTTP_200_OK
        )