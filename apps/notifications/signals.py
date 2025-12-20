# Python modules
from typing import Any

# Django modules
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Project modules
from .models import Notification
from apps.posts.models import Like, Comment


@receiver(post_save, sender=Like)
def create_like_notification(
    sender: type[Like],
    instance: Like,
    created: bool,
    **kwargs: dict[str, Any]
) -> None:
    """Create notification when someone likes a post."""
    if created and instance.post.author != instance.user:
        Notification.objects.create(
            user=instance.post.author,
            actor=instance.user,
            notification_type='like',
            post=instance.post,
            like=instance,
            message=f"{instance.user.username} liked your post"
        )


@receiver(post_save, sender=Comment)
def create_comment_notification(
    sender: type[Comment],
    instance: Comment,
    created: bool,
    **kwargs: dict[str, Any]
) -> None:
    """Creates notification when someone comments on a post or replies to a comment"""
    if created:
        if instance.parent:
            if instance.parent.author != instance.author:
                Notification.objects.create(
                    user=instance.parent.author,
                    actor=instance.author,
                    notification_type='reply',
                    post=instance.post,
                    comment=instance,
                    message=f"{instance.author.username} replied to your comment"
                )
        else:
            if instance.post.author != instance.author:
                Notification.objects.create(
                    user=instance.post.author,
                    actor=instance.author,
                    notification_type='comment',
                    post=instance.post,
                    comment=instance,
                    message=f"{instance.author.username} commented on your post"
                )

