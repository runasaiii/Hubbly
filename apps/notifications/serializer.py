# DRF modules
from rest_framework import serializers

# Project modules
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    organizer_username = serializers.ReadOnlyField(source='organizer.username')
    community_slug = serializers.ReadOnlyField(source='community.slug')

    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'organizer_username',
            'community_slug',
        ]
        read_only_fields = ['id']

