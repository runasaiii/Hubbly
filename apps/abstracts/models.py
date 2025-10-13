#Django modules
from django.db.models import Model, DateTimeField

class AbstractBaseModule(Model):
    """
    Abstract base model ith common fields.
    """
    created_at = DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True