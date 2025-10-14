from django.shortcuts import render
from rest_framework import generics
from django.views.generic import ListView, DetailView
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
