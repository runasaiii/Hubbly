# Pthon modules
import uuid

#Django models
from django.db import models
from django.conf import settings

# Project modules
from apps.abstracts.models import AbstractBaseModel

class Notification(AbstractBaseModel):
    """
         Notification model ith common fields.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'notifications'
    )

