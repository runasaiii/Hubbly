# Django modules
from django.contrib.admin import ModelAdmin, register

# Project modules
from .models import Notification


@register(Notification)
class NotificationsAdmin(ModelAdmin):
    """Admin configuration for Notification model."""
    
    list_display = ('id', 'user', 'type', 'title', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('user__email', 'user__username', 'title', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('id', 'user', 'type', 'title', 'message')
        }),
        ('Статус', {
            'fields': ('is_read', 'created_at', 'updated_at', 'deleted_at')
        }),
        ('Связанные объекты', {
            'fields': ('link', 'related_object_id', 'related_object_type'),
            'classes': ('collapse',)
        }),
    )