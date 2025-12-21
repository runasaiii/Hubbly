# Python modules
from typing import Any

# DRF modules
from rest_framework import generics
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.permissions import IsAuthenticated

# Django modules
from django.views.generic import ListView, DetailView

# Project modules
from .models import Notification
from .serializer import NotificationSerializer


class NotificationListView(generics.ListCreateAPIView):
    """Notification List View controller."""
    
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> Any:
        """Get notifications queryset filtered by current user."""
        queryset = Notification.objects.filter(
            deleted_at__isnull=True,
            user=self.request.user
        )
        
        return queryset.order_by('-created_at')

    def get_serializer_context(self) -> dict[str, Any]:
        """Add request to serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer: NotificationSerializer) -> None:
        """Set user to current user when creating notification."""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

