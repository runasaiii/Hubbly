# Python modules
import uuid

# Django modules
from django.db import models
from django.conf import settings

# Project modules
from apps.abstracts.models import AbstractBaseModel


class Notification(AbstractBaseModel):
    """Notification model with common fields"""
    
    TYPE_CHOICES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('reply', 'Reply'),
        ('follow', 'Follow'),
        ('mention', 'Mention'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text='User who receives the notification'
    )
    actor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_sent',
        help_text='User who triggered the notification'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        help_text='Type of notification'
    )
    post = models.ForeignKey(
        to='posts.Post',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text='Related post if notification is about a post'
    )
    comment = models.ForeignKey(
        to='posts.Comment',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text='Related comment if notification is about a comment'
    )
    like = models.ForeignKey(
        to='posts.Like',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text='Related like if notification is about a like'
    )
    is_read = models.BooleanField(
        default=False,
        help_text='Whether the notification has been read'
    )
    message = models.TextField(
        blank=True,
        help_text='Custom notification message'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'created_at']),
        ]

    def __str__(self) -> str:
        return f"{self.actor.username} {self.get_notification_type_display()} - {self.user.username}"

    def get_message(self) -> str:
        """Generate notification message based on type"""
        if self.message:
            return self.message
        
        actor_name = self.actor.username
        if self.notification_type == 'like':
            return f"{actor_name} liked your post"
        elif self.notification_type == 'comment':
            return f"{actor_name} commented on your post"
        elif self.notification_type == 'reply':
            return f"{actor_name} replied to your comment"
        elif self.notification_type == 'follow':
            return f"{actor_name} started following you"
        elif self.notification_type == 'mention':
            return f"{actor_name} mentioned you"
        return f"{actor_name} interacted with your content"

