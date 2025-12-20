# Python modules
from typing import Any

# DRF modules
from rest_framework import generics, status
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# Django modules
from django.db.models import QuerySet
from django.views.generic import ListView, DetailView

# Project modules
from .models import Notification
from .serializer import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """Notification List view controller"""
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Notification]:
        """Get notifications for current user"""
        return (
            Notification.objects
            .filter(user=self.request.user, deleted_at__isnull=True)
            .select_related('actor', 'post', 'comment', 'like')
            .order_by('-created_at')
        )

    def get_serializer_context(self) -> dict[str, Any]:
        """Add request to serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class NotificationViewSet(ViewSet):
    """ViewSet for handling notification related endpoints"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self) -> QuerySet[Notification]:
        """Get notifications for current user"""
        return (
            Notification.objects
            .filter(user=self.request.user, deleted_at__isnull=True)
            .select_related('actor', 'post', 'comment', 'like')
            .order_by('-created_at')
        )

    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get list of notifications for current user."""
        queryset = self.get_queryset()
        
        is_read = request.query_params.get('is_read', None)
        if is_read is not None:
            is_read_bool = is_read.lower() == 'true'
            queryset = queryset.filter(is_read=is_read_bool)
        
        notification_type = request.query_params.get('notification_type', None)
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)

        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return DRFResponse(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(
        self,
        request: DRFRequest,
        pk: str | None = None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get single notification."""
        try:
            notification = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(notification, context={'request': request})
            return DRFResponse(data=serializer.data, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return DRFResponse(
                data={'detail': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['patch'])
    def mark_read(
        self,
        request: DRFRequest,
        pk: str | None = None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Mark notification as read."""
        try:
            notification = self.get_queryset().get(pk=pk)
            notification.is_read = True
            notification.save(update_fields=['is_read'])
            serializer = self.serializer_class(notification, context={'request': request})
            return DRFResponse(data=serializer.data, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return DRFResponse(
                data={'detail': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def mark_all_read(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Mark all notifications as read"""
        updated = self.get_queryset().filter(is_read=False).update(is_read=True)
        return DRFResponse(
            data={'updated': updated},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def unread_count(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_read=False).count()
        return DRFResponse(
            data={'unread_count': count},
            status=status.HTTP_200_OK
        )

