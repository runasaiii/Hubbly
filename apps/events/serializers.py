# DRF modules
from rest_framework import serializers

# Project modules
from .models import Event, EventApplication


class EventSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for EventSerializer
    """
    organizer_username = serializers.ReadOnlyField(source='organizer.username')
    community_slug = serializers.ReadOnlyField(source='community.slug')

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'start_at',
            'end_at',
            'capacity',
            'status',
            'organizer',
            'organizer_username',
            'community',
            'community_slug',
            'requires_approval',
            'questions',
        ]
        read_only_fields = ['id']


class EventApplicationSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for EventApplicationSerializer
    """
    event_title = serializers.ReadOnlyField(source='event.title')
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = EventApplication
        fields = [
            'id',
            'event',
            'event_title',
            'user',
            'user_username',
            'status',
            'answers',
            'applied_at',
            'reviewed_at',
            'reviewed_by',
        ]
        read_only_fields = ['id', 'applied_at']


