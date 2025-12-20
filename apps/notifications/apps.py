# Django modules
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Notifications app configuration"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.notifications'

    def ready(self) -> None:
        """Import signals when app is ready."""
        import apps.notifications.signals
