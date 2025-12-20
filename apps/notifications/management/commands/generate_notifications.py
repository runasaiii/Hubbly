# Python modules
from typing import Any
from random import choice
from datetime import datetime

# Django modules
from django.core.management.base import BaseCommand

# Project modules
from apps.notifications.models import Notification
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Generate notifications for testing"

    def __generate_notifications(self, notification_count: int = 1000) -> None:
        users = list(CustomUser.objects.all())
        
        if not users:
            self.stdout.write(self.style.ERROR("No users found. Create users first"))
            return
        
        notifications_before = Notification.objects.count()
        created_notifications = []
        
        for i in range(notification_count):
            user = choice(users)
            
            notification = Notification(user=user)
            created_notifications.append(notification)
        
        Notification.objects.bulk_create(created_notifications, ignore_conflicts=True)
        notifications_after = Notification.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {notifications_after - notifications_before} notifications.")
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        start_time = datetime.now()
        
        self.__generate_notifications(notification_count=1000)
