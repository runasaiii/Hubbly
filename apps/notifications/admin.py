from django.contrib.admin import ModelAdmin, register

from .models import Notification

#register Notification App
@register(Notification)
class NotificationsAdmin(ModelAdmin):
    """
    Notifications Admin configuration
    """
    ...