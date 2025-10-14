#Django modules
from django.db import models
import uuid

#App modules
from django.contrib.auth.models import AbstractUser as Abs
from apps.abstracts.models import AbstractBaseModule

class User(Abs):
    """
    User model ith common fields.
    """
    MAX_LENGTH = 150
    id = models.UUIDField(
        primary_key = True, 
        default = uuid.uuid4, 
        editable = False,
        )
    username = models.CharField(
        max_length = MAX_LENGTH, 
        unique = True,
        )
    email = models.EmailField(
        unique = True,
        )
    is_active = models.BooleanField(
        default = True,
        )
    created_at = models.DateTimeField(
        auto_now_add = True,
        )
    updated_at = models.DateTimeField(
        auto_now = True,
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    """
    Profile model ith common fields.
    """
    MAX_LENGTH = 100
    user = models.OneToOneField(
        to = User,
        on_delete = models.CASCADE, 
        related_name = 'profile'
    )
    display_name = models.CharField(
        max_length = MAX_LENGTH,
        blank = True
    )
    bio = models.TextField(blank = True)
    location = models.CharField(
        max_length = MAX_LENGTH,
        blank = True
    )
    interests = models.JSONField(
        default = list, 
        blank = True
    )
    is_verified = models.BooleanField(default = False)
    avatar = models.URLField(
        blank = True,
        null = True
    )


    def __str__(self):
        return self.display_name or str(self.user.username)

class Media(AbstractBaseModule):
    """
    Media model ith common fields.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='media',
    )
    media_type = models.CharField()
    def __str__(self):
        return f"{self.media_type}"