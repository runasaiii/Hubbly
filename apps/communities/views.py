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
)

#App modules
from .models import Community
from .serializers import CommunitySerializer

# Python Modules
from typing import Any

class CommunityListView(generics.ListCreateAPIView):
    """
    Community List View controller
    """
    queryset: Community = Community.objects.all()
    serializer_class: CommunitySerializer = CommunitySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Community Detail View controller
    """
    queryset: Community = Community.objects.all()
    serializer_class: CommunitySerializer = CommunitySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CommunityPageListView(ListView):
    """
    Community Page List View controller
    """
    model: Community = Community
    template_name = 'communities/community_list.html'
    context_object_name = 'communities'


class CommunityPageDetailView(DetailView):
    """
    Community Page Detail View controller
    """
    model: Community = Community
    template_name = 'communities/community_detail.html'
    context_object_name = 'community'


class CommunityViewSet(ViewSet):
    """
    Creating endpoints for Communities
    """

    def get_queryset(self):
        """
        Get Queryset
        """
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
    )-> DRFResponse:
        """
        Creating GET request
        """
        all_communities: QuerySet[Community]=self.get_queryset().all()

        serializer: CommunitySerializer = CommunitySerializer(
            all_communities,
            many=True,
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
    )-> DRFResponse:

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
    )-> DRFResponse:
        """
        Implementing PATCH endpoint
        """
        try:
            community: Community = self.get_queryset().get(id=kwargs['pk'])
        except Community.DoesNotExist:
            return DRFResponse(
                {'detail': 'This Community Does Not Exist'},
                status=HTTP_400_BAD_REQUEST
            )

        serializer: CommunitySerializer = CommunitySerializer(
            data=request.data,
            instance=community,
            partial=True,
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
    )-> DRFResponse:
        """
        Implementing DELETE endpoint
        """
        try:
            community: Community = self.get_queryset().get(id=kwargs['pk'])
        except Community.DoesNotExist:
            return DRFResponse(
                {'detail': 'This Community Does Not Exist'},
                status=HTTP_400_BAD_REQUEST
            )
        community.delete()

        return DRFResponse(
            status=HTTP_204_NO_CONTENT
        )
