#Django modules
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance whenever a new User is created.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the Profile instance whenever the User is saved.
    """
    instance.profile.save()