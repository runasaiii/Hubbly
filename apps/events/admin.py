from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Event, EventApplication

#register Event App
@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = (
        'id', 'title', 'community', 'organizer', 'start_at', 'end_at', 'status'
    )
    list_filter = ('status', 'community', 'requires_approval')
    search_fields = ('title', 'community__name', 'organizer__email', 'organizer__username')
    date_hierarchy = 'start_at'

#register Event Application App
@admin.register(EventApplication)
class EventApplicationAdmin(ModelAdmin):
    list_display = ('id', 'event', 'user', 'status', 'applied_at', 'reviewed_at')
    list_filter = ('status',)
    search_fields = ('event__title', 'user__email', 'user__username')