# Python modules
from typing import Any

# Django Modules
from django.db.models import QuerySet, Count
from django.views.generic import ListView, DetailView

# Django Rest Framework Modules
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND
)

# Project Modules
from .permissions import IsEventOrganizer
from .models import Event
from .serializers import (
    EventSerializer,
    EventNotFoundSerializer,
    EventResponseSerializer,
)
from .filters import EventFilter

# Swagger modules
from drf_spectacular.utils import extend_schema, OpenApiResponse


class EventViewSet(ViewSet):
    """ViewSet for handling event related endpoints"""

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy'):
            permission_classes = (IsAuthenticated, IsEventOrganizer)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    serializer_class = EventSerializer
    filterset_class = EventFilter

    def get_queryset(self) -> QuerySet[Event]:
        """Get optimized queryset with organizer and annotations"""
        return (
            Event.objects
            .filter(deleted_at__isnull=True)
            .select_related('organizer', 'community')
            .annotate(
                applications_count=Count('applications', distinct=True)
            )
        )


    @extend_schema(
        summary="List all events",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successfully returns list of events",
                response=EventSerializer(many=True)
            ),
        }
    )
    def list(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get list of all events with filtering"""

        queryset = self.get_queryset()
        
        filterset = self.filterset_class(request.query_params, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        
        ordering = request.query_params.get('ordering', 'start_at')
        if ordering:
            queryset = queryset.order_by(*ordering.split(','))

        serializer: EventSerializer = EventSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )


    @extend_schema(
        summary="Create a new event",
        responses={
            HTTP_201_CREATED: OpenApiResponse(
                description="Event successfully created",
                response=EventSerializer
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid input data",
                response=EventResponseSerializer,
            ),
        }
    )
    def create(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Create a new event"""

        serializer: EventSerializer = EventSerializer(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

        serializer.save(organizer=request.user)

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED,
        )


    @extend_schema(
        summary="Partially update an event",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Event successfully updated",
                response=EventSerializer
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Event with this ID does not exist",
                response=EventNotFoundSerializer
            ),
        }
    )
    def partial_update(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Partially update an event"""

        try:
            event: Event = self.get_queryset().get(id=kwargs['id'])
        except Event.DoesNotExist:
            return DRFResponse(
                data={
                    f"Event with that id={kwargs['pk']} does not exists"
                },
                status=HTTP_404_NOT_FOUND
            )

        serializer: EventSerializer = EventSerializer(
            data=request.data,
            instance=event,
            partial=True,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK,
        )


    @extend_schema(
        summary="Delete an event",
        responses={
            HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Event successfully deleted"
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Event with this ID does not exist",
                response=EventNotFoundSerializer,
            ),
        }
    )
    def destroy(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Creating a delete request"""

        try:
            event: Event = self.get_queryset().get(id=kwargs['id'])
        except Event.DoesNotExist:
            return DRFResponse(
                data={
                    'pk': [f'Event with pk={kwargs["pk"]} does not exist']
                },
                status=HTTP_404_NOT_FOUND
            )

        event.delete()

        return DRFResponse(
            status=HTTP_204_NO_CONTENT
        )


    @extend_schema(
        summary="Retrieve a single event by ID",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successfully returns the requested event",
                response=EventSerializer,
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Event with this ID does not exist",
                response=EventNotFoundSerializer,
            ),
        }
    )
    def retrieve(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get single event by id"""

        try:
            event: Event = self.get_queryset().get(id=kwargs['id'])
        except Event.DoesNotExist:
            return DRFResponse(
                data={'detail': f'Event with id={kwargs["id"]} does not exist'},
                status=HTTP_404_NOT_FOUND
            )

        serializer: EventSerializer = EventSerializer(
            event,
            context={'request': request}
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

