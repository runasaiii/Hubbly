# Python modules
import uuid

#Django modules
from django.db import models
from django.conf import settings

#App modules
from apps.communities.models import Community


class Event(models.Model):
    """
              Event model ith common fields.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    capacity = models.PositiveIntegerField(
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='draft'
    )
    organizer = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'events_organized'
    )
    community = models.ForeignKey(
        to = Community,
        on_delete = models.CASCADE,
        related_name = 'events',
    )
    requires_approval = models.BooleanField(default=False)
    questions = models.JSONField(
        default=list,
        blank=True
    )

    def __str__(self):
        return self.title
    

class EventApplication(models.Model):
    """
     Event application model ith common fields.
    """
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    event = models.ForeignKey(
        to = Event,
        on_delete = models.CASCADE,
        related_name = 'applications'
    )
    user = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    status = models.CharField(
        max_length = 15,
        choices = STATUS_CHOICES,
        default = 'pending'
    )
    answers = models.JSONField(
        default = dict,
        blank = True
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(
        null = True,
        blank = True
    )
    reviewed_by = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        null=True,
        blank=True,
        related_name = 'event_applications_reviewed'
    )

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"Application of {self.user.username} for {self.event.title}"