# DRF modules
from rest_framework import serializers

# Project modules
from .models import Event, EventApplication


class EventSerializer(serializers.ModelSerializer):
    """Serializer for event model"""
    
    organizer_username: serializers.ReadOnlyField = serializers.ReadOnlyField(source='organizer.username')

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
            'requires_approval',
            'questions',
        ]
        read_only_fields = ['id', 'organizer', 'organizer_username']


class EventApplicationSerializer(serializers.ModelSerializer):
    """Serializer for EventApplication model"""
    
    event_title: serializers.ReadOnlyField = serializers.ReadOnlyField(source='event.title')
    user_username: serializers.ReadOnlyField = serializers.ReadOnlyField(source='user.username')

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


