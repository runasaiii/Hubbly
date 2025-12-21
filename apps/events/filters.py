# Python modules
from typing import Any

# Django modules
from django.db.models import Q
from django_filters import rest_framework as filters

# Project modules
from .models import Event


class EventFilter(filters.FilterSet):
    """Filter for event model"""
    
    community = filters.UUIDFilter(
        field_name='community', 
        lookup_expr='exact'
        )
    organizer = filters.UUIDFilter(
        field_name='organizer', 
        lookup_expr='exact'
        )
    status = filters.ChoiceFilter(
        field_name='status',
        choices=Event.STATUS_CHOICES,
        lookup_expr='exact'
    )
    requires_approval = filters.BooleanFilter(
        field_name='requires_approval', 
        lookup_expr='exact'
        )
    search = filters.CharFilter(method='filter_search')

    class Meta:
        model = Event
        fields = ['community', 'organizer', 'status', 'requires_approval', 'search']

    def filter_search(self, queryset: Any, name: str, value: str) -> Any:
        """Search in event title and description"""
        if value:
            return queryset.filter(
                Q(title__icontains=value) | Q(description__icontains=value)
            )
        return queryset

