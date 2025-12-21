# Python modules
import uuid

# Django modules
from django.db import models
from django.conf import settings

# Project modules
from apps.abstracts.models import AbstractBaseModel

class Notification(AbstractBaseModel):
    """Notification model with common fields."""
    
    TYPE_CHOICES = [
        ('comment', 'Comment'),
        ('like', 'Like'),
        ('follow', 'Follow'),
        ('event', 'Event'),
        ('community', 'Community'),
        ('post', 'Post'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='post'
    )
    title = models.CharField(
        max_length=200,
        blank=True
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.URLField(
        blank=True,
        null=True
    )
    related_object_id = models.UUIDField(
        null=True,
        blank=True,
        help_text="ID связанного объекта (пост, комментарий, событие и тд)"
    )
    related_object_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Тип связанного объекта (post, comment, event и тд)"
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.type} notification for {self.user.username}"

