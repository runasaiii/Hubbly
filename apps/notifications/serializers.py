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
    """Serializer for notification model"""

    actor_username = ReadOnlyField(source='actor.username')
    actor_full_name = ReadOnlyField(source='actor.full_name')
    post_id = ReadOnlyField(source='post.id')
    post_content_preview = SerializerMethodField()
    comment_id = ReadOnlyField(source='comment.id')
    comment_content_preview = SerializerMethodField()
    message = SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'actor',
            'actor_username',
            'actor_full_name',
            'notification_type',
            'post',
            'post_id',
            'post_content_preview',
            'comment',
            'comment_id',
            'comment_content_preview',
            'like',
            'is_read',
            'message',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'message']

    def get_post_content_preview(self, obj: Notification) -> str | None:
        """Get preview of post content"""
        if obj.post:
            content = obj.post.content
            return content[:100] + '...' if len(content) > 100 else content
        return None

    def get_comment_content_preview(self, obj: Notification) -> str | None:
        """Get preview of comment content"""
        if obj.comment:
            content = obj.comment.content
            return content[:100] + '...' if len(content) > 100 else content
        return None

    def get_message(self, obj: Notification) -> str:
        """Get notification message"""
        return obj.get_message()


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

