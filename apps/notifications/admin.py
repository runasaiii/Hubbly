# Django modules
from django.contrib.admin import ModelAdmin, register

# Project modules
from .models import Notification


@register(Notification)
class NotificationsAdmin(ModelAdmin):
    """Admin configuration for notification model"""
    
    list_display = ('id', 'user', 'actor', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__email', 'user__username', 'actor__email', 'actor__username', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'actor', 'notification_type', 'is_read')
        }),
        ('Related Objects', {
            'fields': ('post', 'comment', 'like')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at')
        }),
    )