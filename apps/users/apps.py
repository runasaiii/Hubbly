# Django Modules
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    AppConfig for UsersConfig
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        import apps.users.signals
