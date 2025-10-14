from django.shortcuts import render
from rest_framework import generics
from django.views.generic import ListView, DetailView
from .models import Notification
from .serializer import NotificationSerializer
class NotificationListView(generics.ListCreateAPIView):
    """
    Event List View controller
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

