#Django Modules
from django.contrib.admin import ModelAdmin, register

#Project modules
from .models import Notification

@register(Notification)
class NotificationsAdmin(ModelAdmin):
    """
    Notifications Admin configuration
    """
    ...