# Python modules
from typing import Any

# DRF modules
from rest_framework import serializers

# Project modules
from .models import Notification
from apps.users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notification model"""
    
    actor_username = serializers.ReadOnlyField(source='actor.username')
    actor_full_name = serializers.ReadOnlyField(source='actor.full_name')
    post_id = serializers.ReadOnlyField(source='post.id')
    post_content_preview = serializers.SerializerMethodField()
    comment_id = serializers.ReadOnlyField(source='comment.id')
    comment_content_preview = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    
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

