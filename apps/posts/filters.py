# Python modules
from typing import Any

# Django modules
from django_filters import rest_framework as filters

# Project modules
from .models import Post


class PostFilter(filters.FilterSet):
    """Filter for post model"""
    
    community = filters.UUIDFilter(field_name='community', lookup_expr='exact')
    author = filters.UUIDFilter(field_name='author', lookup_expr='exact')
    pinned = filters.BooleanFilter(field_name='pinned', lookup_expr='exact')
    tags = filters.CharFilter(field_name='tags__name', lookup_expr='icontains')
    search = filters.CharFilter(method='filter_search')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['community', 'author', 'pinned', 'tags', 'search']

    def filter_search(self, queryset: Any, name: str, value: str) -> Any:
        """Search in post content."""
        if value:
            return queryset.filter(content__icontains=value)
        return queryset

