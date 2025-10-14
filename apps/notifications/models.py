#Django models
import uuid
from django.db import models
#App modules
from apps.users.models import User
from apps.abstracts.models import AbstractBaseModule

class Notification(AbstractBaseModule):
    """
         Notification model ith common fields.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user_id = models.ForeignKey(
        to = User,
        on_delete = models.CASCADE,
        related_name = 'userid'
    )

