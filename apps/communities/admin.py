# Django modules
from django.contrib import admin
from unfold.admin import ModelAdmin

# Project modules
from .models import Community, CommunityMembership


@admin.register(Community)
class CommunityAdmin(ModelAdmin):
    """Admin configuration for Community model."""
    
    list_display = ('id', 'name', 'visibility', 'owner', 'created_at')
    list_filter = ('visibility',)
    search_fields = ('name', 'owner__email', 'owner__username')


@admin.register(CommunityMembership)
class CommunityMembershipAdmin(ModelAdmin):
    """Admin configuration for CommunityMembership model."""
    
    list_display = ('id', 'user', 'community', 'role', 'status', 'joined_at')
    list_filter = ('role', 'status')
    search_fields = ('user__email', 'user__username', 'community__name')
