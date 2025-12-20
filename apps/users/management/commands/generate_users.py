# Python modules
from typing import Any
from random import choice, choices
from datetime import datetime

#  Django modules
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import QuerySet

# Project modules
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Generate users for testing purpose"

    EMAIL_DOMAINS = {
        "example.com",
        "test.com",
        "sample.org",
        "demo.net",
        "mail.com",
    }
    SOME_WORDS = {
        "lorem",
        "ipsum",
        "dolor",
        "sit",
        "amet",
        "consectetur",
        "adipiscing",
        "elit",
        "sed",
        "do",
        "eiusmod",
        "tempor",
        "incididunt",
        "ut",
        "labore",
        "et",
        "dolore",
        "magna",
        "aliqua",
    }

    def __generate_users(self, user_count: int = 1000) -> None:
        """
        Generate users for testing purposes.
        """
        USER_PASSWORD = make_password(password="12345")
        created_users: list[CustomUser] = []
        users_before: int = CustomUser.objects.count()
        i: int
        for i in range(user_count):
            username: str = f'username {i+1}'
            full_name: str = f"user {i+1}"
            email: str = f"user{i+1}@{choice(list(self.EMAIL_DOMAINS))}"
            created_users.append(
                CustomUser(
                    username = username,
                    full_name = full_name,
                    email = email,
                    password = USER_PASSWORD,
                )
            )
        CustomUser.objects.bulk_create(created_users, ignore_conflicts = True)
        users_after: int = CustomUser.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {users_after - users_before} users."
            )
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """ Commands entry point. """
        start_time: datetime = datetime.now()
        self.__generate_users(user_count=1000)
