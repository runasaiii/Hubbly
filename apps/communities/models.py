#Django modules
from django.db import models
from django.conf import settings
import uuid

#App modules
from apps.abstracts.models import AbstractBaseModel

class Community(AbstractBaseModel):
    """
        Community model ith common fields.
    """
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('secret', 'Secret')
    ]

    MAX_LENGTH = 100
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    name = models.CharField(max_length=MAX_LENGTH)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    visibility = models.CharField(
        max_length=10, 
        choices=VISIBILITY_CHOICES, 
        default='public'
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_communities')

    def __str__(self):
        return self.name
    

class CommunityMembership(models.Model):
    """
          Community membership model ith common fields.
    """
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('organizer', 'Organizer')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('banned', 'Banned')
    ]

    MAX_LENGTH = 100
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        to = settings.AUTH_USER_MODEL, 
        on_delete = models.CASCADE, 
        related_name = 'community_memberships'
    )
    community = models.ForeignKey(
        to = Community, 
        on_delete=models.CASCADE, 
        related_name='memberships'
    )
    role = models.CharField(
        max_length=MAX_LENGTH, 
        choices=ROLE_CHOICES)
    status = models.CharField(
        max_length=MAX_LENGTH, 
        choices=STATUS_CHOICES
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'community')

    def __str__(self):
        return f"{self.user.username} in {self.community.name} as {self.role}"