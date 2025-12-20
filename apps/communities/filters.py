# Python modules
from typing import Any

# Django modules
from django_filters import rest_framework as filters

# Project modules
from .models import Community


class CommunityFilter(filters.FilterSet):
    """Filter for Community model."""
    
    visibility = filters.ChoiceFilter(
        field_name='visibility',
        choices=Community.VISIBILITY_CHOICES,
        lookup_expr='exact'
    )
    owner = filters.UUIDFilter(field_name='owner', lookup_expr='exact')
    search = filters.CharFilter(method='filter_search')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Community
        fields = ['visibility', 'owner', 'search']

    def filter_search(self, queryset: Any, name: str, value: str) -> Any:
        """Search in community name and description."""
        if value:
            return queryset.filter(
                name__icontains=value
            ) | queryset.filter(
                description__icontains=value
            )
        return queryset

