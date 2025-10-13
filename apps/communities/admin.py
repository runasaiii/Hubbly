from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Community, CommunityMembership


@admin.register(Community)
class CommunityAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug', 'visibility', 'owner', 'created_at')
    list_filter = ('visibility',)
    search_fields = ('name', 'slug', 'owner__email', 'owner__username')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CommunityMembership)
class CommunityMembershipAdmin(ModelAdmin):
    list_display = ('id', 'user', 'community', 'role', 'status', 'joined_at')
    list_filter = ('role', 'status')
    search_fields = ('user__email', 'user__username', 'community__name')
