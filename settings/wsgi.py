import os
from django.core.wsgi import get_wsgi_application
from settings.conf import ENV_ID, ENV_POSSIBLE_OPTIONS


assert ENV_ID in ENV_POSSIBLE_OPTIONS, (
    f"ENV_ID should be one of {ENV_POSSIBLE_OPTIONS}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.env.{ENV_ID}')

application = get_wsgi_application()
