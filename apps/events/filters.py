# Python modules
from typing import Any

# Django modules
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
    start_after = filters.DateTimeFilter(
        field_name='start_at', 
        lookup_expr='gte'
        )
    start_before = filters.DateTimeFilter(
        field_name='start_at',  
        lookup_expr='lte'
        )
    search = filters.CharFilter(method='filter_search')

    class Meta:
        model = Event
        fields = ['community', 'organizer', 'status', 'requires_approval', 'search']

    def filter_search(self, queryset: Any, name: str, value: str) -> Any:
        """Search in event title and description"""
        if value:
            return queryset.filter(
                title__icontains=value
            ) | queryset.filter(
                description__icontains=value
            )
        return queryset

