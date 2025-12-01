# DRF modules
from rest_framework import generics

# Django modules
from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Project modules
from .models import Notification
from .serializer import NotificationSerializer


class NotificationListView(generics.ListCreateAPIView):
    """
    Event List View controller
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

