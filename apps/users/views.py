# Python modules
from typing import Any

# Django Rest Framework modules
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action


# Django modules
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView


# Project modules
from .models import CustomUser
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    RegistrationSerializer,
    UserLoginSerializer,
)


def user_list(request):
    """
    User List controller
    """
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)


def user_detail(request, user_id):
    """
    User Detail controller
    """
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=404)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)


class UserPageListView(ListView):
    """
    User Page List View controller
    """
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserPageDetailView(DetailView):
    """
    User Page Detail View controller
    """
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'user_obj'


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom Token Obtain Pair View using CustomTokenObtainPairSerializer
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegistrationView(generics.CreateAPIView):
    """
    User Registration View
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer


# Saya's code for Login Endpoints
class CustomUserViewSet(ViewSet):
    """ Creating Login Endpoints for CustomUser"""

    @action(
        methods=('POST',),
        detail=False,
        url_path='login',
        url_name='login',
        permission_classes = (AllowAny,)
    )
    def login(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],

    ) -> DRFResponse:
        """
                Handle user login.

                Parameters:
                    request: DRFRequest
                        The request object.
                    *args: tuple
                        Additional positional arguments.
                    **kwargs: dict
                        Additional keyword arguments.

                Returns:
                    DRFResponse
                        Response containing user data or error message.
        """
        serializer: UserLoginSerializer = UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user: CustomUser = serializer.validated_data.pop("user")

        #Generate User's tokens
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