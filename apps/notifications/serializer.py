from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    organizer_username = serializers.ReadOnlyField(source='organizer.username')
    community_slug = serializers.ReadOnlyField(source='community.slug')

    class Meta:
        model = Notification
        fields = [
            'id',
            'user_id',
        ]
        read_only_fields = ['id']

