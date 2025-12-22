# DRF modules
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    ReadOnlyField,
    CharField,
    ListField,
)

# Project modules
from .models import Event, EventApplication


class EventSerializer(ModelSerializer):
    """Serializer for event model"""
    
    organizer_username: ReadOnlyField = ReadOnlyField(source='organizer.username')

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


class EventNotFoundSerializer(Serializer):
    """
    Serializer for HTTP 404 Method Not Allowed response.
    """

    detail = CharField()

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "detail",
        )


class EventResponseSerializer(Serializer):
    """
    Serializer for event errors.
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


class EventApplicationSerializer(ModelSerializer):
    """Serializer for EventApplication model"""
    
    event_title: ReadOnlyField = ReadOnlyField(source='event.title')
    user_username: ReadOnlyField = ReadOnlyField(source='user.username')

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


