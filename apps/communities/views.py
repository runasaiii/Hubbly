# Python Modules
from http.client import responses
from typing import Any

#Django modules
from django.db.models import QuerySet, Count, Q
from django.views.generic import ListView, DetailView

# DRF
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated


# App modules
from .permissions import IsCommunityOwner
from .models import Community, CommunityMembership
from .serializers import (
    CommunitySerializer,
    NotFoundSerializer,
    CommunityResponseSerializer,
    CommunityMembershipSerializer,
)
from .filters import CommunityFilter

# Swagger modules
from drf_spectacular.utils import extend_schema, OpenApiResponse


class CommunityViewSet(ViewSet):

    """ViewSet for handling community related endpoints"""
    filterset_class = CommunityFilter

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy'):
            permission_classes = (IsAuthenticated, IsCommunityOwner)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    @extend_schema(
        summary="Get a specific community by ID",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successfully returns the requested community",
                response=CommunitySerializer,
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Community with this ID does not exist",
                response=NotFoundSerializer,
            ),
        }
    )
    def retrieve(self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    )-> DRFResponse:
        """GET /api/communities/<pk>/"""
        try:
            community = self.get_queryset().get(id=kwargs['pk'])
        except Community.DoesNotExist:
            return DRFResponse({'detail': 'Community not found'}, status=HTTP_404_NOT_FOUND)

        serializer = CommunitySerializer(community, context={'request': request})
        return DRFResponse(serializer.data, status=HTTP_200_OK)

    def get_queryset(self) -> QuerySet[Community]:
        """Get optimized queryset with owner, memberships and annotations"""
        from apps.posts.models import Post
        # Count active members + owner (owner is always counted as member)
        return (
            Community.objects
            .filter(deleted_at__isnull=True)
            .select_related('owner')
            .prefetch_related('memberships', 'posts')
            .annotate(
                active_members_count=Count('memberships', filter=Q(memberships__status='active'), distinct=True),
                posts_count=Count('posts', filter=Q(posts__deleted_at__isnull=True), distinct=True)
            )
        )

    @extend_schema(
        summary="List all communities with optional filtering and ordering",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successfully returns a list of communities",
                response=CommunitySerializer(many=True),
            ),
        }
    )
    def list(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get list of all communities with filtering"""
        queryset = self.get_queryset()
        
        filterset = self.filterset_class(request.query_params, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(*ordering.split(','))

        serializer: CommunitySerializer = CommunitySerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(
        summary="Create a new community",
        request=CommunitySerializer,
        responses={
            HTTP_201_CREATED: OpenApiResponse(
                description="Community created successfully",
                response=CommunitySerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid input data",
                response=CommunityResponseSerializer,
            ),
        }
    )
    def create(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Create a new community"""

        serializer: CommunitySerializer = CommunitySerializer(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )

        serializer.save(owner=request.user)

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )

    @extend_schema(
        summary="Partially update a community",
        request=CommunitySerializer,
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Community updated successfully",
                response=CommunitySerializer,
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Community not found",
                response=NotFoundSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid input data",
                response=CommunitySerializer,
            ),
        }
    )
    def partial_update(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Partially update a community"""
        try:
            community: Community = self.get_queryset().get(id=kwargs['pk'])
        except Community.DoesNotExist:
            return DRFResponse(
                {'detail': 'This community doesnt exist'},
                status=HTTP_404_NOT_FOUND
            )

        serializer: CommunitySerializer = CommunitySerializer(
            data=request.data,
            instance=community,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(
        summary="Delete a community",
        responses={
            HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Community deleted successfully",
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Community not found",
                response=NotFoundSerializer,
            ),
        }
    )
    def destroy(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Delete a community"""
        try:
            community: Community = self.get_queryset().get(id=kwargs['pk'])
        except Community.DoesNotExist:
            return DRFResponse(
                {'detail': 'This community doesnt exist'},
                status=HTTP_404_NOT_FOUND
            )
        community.delete()

        return DRFResponse(
            status=HTTP_204_NO_CONTENT
        )

    @extend_schema(
        summary="Join a community",
        responses={
            HTTP_201_CREATED: OpenApiResponse(
                description="Successfully joined the community",
                response=CommunityMembershipSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Already a member or invalid request",
                response=CommunityResponseSerializer,
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Community not found",
                response=NotFoundSerializer,
            ),
        }
    )
    @action(
        methods=['POST'],
        detail=True,
        url_path='join',
        permission_classes=[IsAuthenticated],
    )
    def join(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Join a community - creates membership with appropriate status"""
        try:
            community: Community = self.get_queryset().get(id=kwargs['pk'])
        except Community.DoesNotExist:
            return DRFResponse(
                {'detail': 'Community not found'},
                status=HTTP_404_NOT_FOUND
            )

        existing_membership = CommunityMembership.objects.filter(
            user=request.user,
            community=community
        ).first()

        if existing_membership:
            return DRFResponse(
                {'detail': 'You are already a member of this community'},
                status=HTTP_400_BAD_REQUEST
            )

        if community.owner == request.user:
            return DRFResponse(
                {'detail': 'You are the owner of this community'},
                status=HTTP_400_BAD_REQUEST
            )


        if community.visibility == 'public':
            status = 'active'
        else:
            status = 'pending'

        membership = CommunityMembership.objects.create(
            user=request.user,
            community=community,
            role='member',
            status=status
        )

        serializer = CommunityMembershipSerializer(membership)
        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )

    @extend_schema(
        summary="Get community members",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successfully returns list of community members",
                response=CommunityMembershipSerializer(many=True),
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Community not found",
                response=NotFoundSerializer,
            ),
        }
    )
    @action(
        methods=['GET'],
        detail=True,
        url_path='members',
        permission_classes=[IsAuthenticated],
    )
    def members(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get list of community members including owner"""
        try:
            community: Community = self.get_queryset().get(id=kwargs['pk'])
        except Community.DoesNotExist:
            return DRFResponse(
                {'detail': 'Community not found'},
                status=HTTP_404_NOT_FOUND
            )

        memberships = CommunityMembership.objects.filter(
            community=community,
            status='active'
        ).select_related('user').order_by('joined_at')

        membership_serializer = CommunityMembershipSerializer(memberships, many=True)
        members_list = list(membership_serializer.data)

        owner_in_members = any(m['user'] == str(community.owner.id) for m in members_list)
        if not owner_in_members:
            owner_membership_data = {
                'id': str(community.owner.id),
                'user': str(community.owner.id),
                'user_username': community.owner.username,
                'community': str(community.id),
                'community_name': community.name,
                'role': 'organizer', 
                'status': 'active',
                'joined_at': community.created_at.isoformat() if hasattr(community, 'created_at') and community.created_at else None,
            }
            members_list.insert(0, owner_membership_data)

        return DRFResponse(
            data=members_list,
            status=HTTP_200_OK
        )

    @extend_schema(
        summary="Leave a community",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successfully left the community",
                response=CommunityResponseSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Not a member or cannot leave",
                response=CommunityResponseSerializer,
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Community not found",
                response=NotFoundSerializer,
            ),
        }
    )
    @action(
        methods=['POST'],
        detail=True,
        url_path='leave',
        permission_classes=[IsAuthenticated],
    )
    def leave(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Leave a community - removes membership"""
        try:
            community: Community = self.get_queryset().get(id=kwargs['pk'])
        except Community.DoesNotExist:
            return DRFResponse(
                {'detail': 'Community not found'},
                status=HTTP_404_NOT_FOUND
            )

        if community.owner == request.user:
            return DRFResponse(
                {'detail': 'Community owner cannot leave the community'},
                status=HTTP_400_BAD_REQUEST
            )

        try:
            membership = CommunityMembership.objects.get(
                user=request.user,
                community=community
            )
            membership.delete()
            return DRFResponse(
                {'detail': 'Successfully left the community'},
                status=HTTP_200_OK
            )
        except CommunityMembership.DoesNotExist:
            return DRFResponse(
                {'detail': 'You are not a member of this community'},
                status=HTTP_400_BAD_REQUEST
            )
