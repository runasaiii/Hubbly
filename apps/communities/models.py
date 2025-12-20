# Python modules
import uuid

#Django modules
from django.db import models
from django.conf import settings

# Project modules
from apps.abstracts.models import AbstractBaseModel


class Community(AbstractBaseModel):
    """Community model with common fields"""
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('secret', 'Secret')
    ]
    COMM_NAME_MAX_LENGTH = 50
    MAX_LENGTH = 100
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    name = models.CharField(
        max_length=COMM_NAME_MAX_LENGTH
        )
    description = models.TextField(blank=True)
    visibility = models.CharField(
        choices=VISIBILITY_CHOICES, 
        default='public'
    )
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_communities')

    def __str__(self):
        return self.name
    

class CommunityMembership(models.Model):
    """Community membership model with common fields"""

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
        choices=ROLE_CHOICES)
    status = models.CharField( 
        choices=STATUS_CHOICES
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'community')

    def __str__(self):
        return f"{self.user.username} in {self.community.name} as {self.role}"