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
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_404_NOT_FOUND


# Project Modules
from .models import Event
from .serializers import EventSerializer


class EventListView(generics.ListCreateAPIView):
    """
    Event List View controller
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Event Detail View controller
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventPageListView(ListView):
    """
    Event Page List View
    """
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 20


class EventPageDetailView(DetailView):
    """
    Event Page Detail View controller
    """
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventViewSet(ViewSet):
    """
    Creating Event ViewSet for handling Event-related endpoints
    """
    permission_classes = (IsAuthenticated,)

    def list(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """ Creating GET request"""

        all_events:  QuerySet[Event] = Event.objects.annotate(
            users_count=Count('users', distinct=True)
        ).all()

        serializer: EventSerializer = EventSerializer(
            all_events,
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
    ) -> DRFResponse:
        """ Creating POST request"""

        serializer: EventSerializer = EventSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

        serializer.save()

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
        """ Creating PATCH request"""

        try:
            event: Event = Event.objects.get(id=kwargs['pk'])
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
        """ Creating PATCH request"""

        try:
            event: Event = Event.objects.get(id=kwargs['pk'])
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
