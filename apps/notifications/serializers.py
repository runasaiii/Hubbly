# Python modules
from typing import Any

# DRF modules
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    ReadOnlyField,
    SerializerMethodField,
    CharField,
    ListField,
)

# Project modules
from .models import Notification
from apps.users.serializers import UserSerializer


class NotificationSerializer(ModelSerializer):
    """Serializer for Notification model."""

    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'type',
            'title',
            'message',
            'is_read',
            'link',
            'related_object_id',
            'related_object_type',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class NotificationErrorSerializer(Serializer):
    """
        Serializer for HTTP 404 Method Not Allowed response.
        """

    detail = CharField()

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "detail",
        )


class NotificationRespondSerializer(Serializer):
    """
        Serializer for community errors.
        """

    event_title = ListField(
        child=CharField(),
        required=False,
    )
    event = ListField(
        child=CharField(),
        required=False,
    )

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "event",
            "event_title",
        )

