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
from django_filters.rest_framework import DjangoFilterBackend


# Project Modules
from .models import Event
from .serializers import EventSerializer
from .filters import EventFilter


class EventListView(generics.ListCreateAPIView):
    """Event List View controller."""
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend]
    ordering_fields = ['start_at', 'created_at']
    ordering = ['start_at']
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self) -> dict[str, Any]:
        """Add request to serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer: EventSerializer) -> None:
        """Set organizer to current user when creating event."""
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Event Detail View controller."""
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_context(self) -> dict[str, Any]:
        """Add request to serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class EventPageListView(ListView):
    """Event Page List View."""
    
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 20


class EventPageDetailView(DetailView):
    """Event Page Detail View controller."""
    
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventViewSet(ViewSet):
    """ViewSet for handling Event-related endpoints."""
    
    permission_classes = (IsAuthenticated,)
    filterset_class = EventFilter

    def get_queryset(self) -> QuerySet[Event]:
        """Get optimized queryset with organizer and annotations."""
        return (
            Event.objects
            .filter(deleted_at__isnull=True)
            .select_related('organizer', 'community')
            .annotate(
                applications_count=Count('applications', distinct=True)
            )
        )
    def list(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get list of all events with filtering."""

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


    def create(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Create a new event."""

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


    def partial_update(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Partially update an event."""

        try:
            event: Event = self.get_queryset().get(id=kwargs['pk'])
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


    def destroy(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Creating DELETE request."""

        try:
            event: Event = self.get_queryset().get(id=kwargs['pk'])
        except Event.DoesNotExist:
            return DRFResponse(
                data={
                    'pk': [f'Event with pk={kwargs["pk"]} does not exist.']
                },
                status=HTTP_404_NOT_FOUND
            )

        event.delete()

        return DRFResponse(
            status=HTTP_204_NO_CONTENT
        )
