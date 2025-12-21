#Django modules
from django.db.models import QuerySet, Count
from django.views.generic import ListView, DetailView

#DRF
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

# App modules
from .models import Community
from .serializers import CommunitySerializer
from .filters import CommunityFilter

# Python Modules
from typing import Any


class CommunityListView(generics.ListCreateAPIView):
    """Community List View controller."""
    
    queryset = Community.objects.filter(deleted_at__isnull=True)
    serializer_class = CommunitySerializer
    filterset_class = CommunityFilter
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_serializer_context(self) -> dict[str, Any]:
        """Add request to serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Community Detail View controller."""
    
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def get_serializer_context(self) -> dict[str, Any]:
        """Add request to serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CommunityPageListView(ListView):
    """Community Page List View controller."""
    
    model = Community
    template_name = 'communities/community_list.html'
    context_object_name = 'communities'


class CommunityPageDetailView(DetailView):
    """Community Page Detail View controller."""
    
    model = Community
    template_name = 'communities/community_detail.html'
    context_object_name = 'community'


class CommunityViewSet(ViewSet):
    """ViewSet for handling Community-related endpoints."""
    
    filterset_class = CommunityFilter

    def get_queryset(self) -> QuerySet[Community]:
        """Get optimized queryset with owner, memberships and annotations."""
        return (
            Community.objects
            .filter(deleted_at__isnull=True)
            .select_related('owner')
            .prefetch_related('memberships')
            .annotate(
                users_count=Count('memberships', distinct=True)
            )
        )


    def list(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get list of all communities with filtering."""
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


    def create(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Create a new community."""

        serializer: CommunitySerializer = CommunitySerializer(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )


    def partial_update(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Partially update a community."""
        try:
            community: Community = self.get_queryset().get(id=kwargs['pk'])
        except Community.DoesNotExist:
            return DRFResponse(
                {'detail': 'This Community Does Not Exist'},
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


    def destroy(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Delete a community."""
        try:
            community: Community = self.get_queryset().get(id=kwargs['pk'])
        except Community.DoesNotExist:
            return DRFResponse(
                {'detail': 'This Community Does Not Exist'},
                status=HTTP_404_NOT_FOUND
            )
        community.delete()

        return DRFResponse(
            status=HTTP_204_NO_CONTENT
        )
