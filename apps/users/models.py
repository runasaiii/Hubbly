#Django modules
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#App modules
from apps.abstracts.models import AbstractBaseModule
class User(PermissionsMixin, AbstractBaseUser, AbstractBaseModule):
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
    updated_at = models.DateTimeField(
        auto_now = True,
        )
    is_staff = models.BooleanField(
        default=False,
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
        'users.User',  # строковая ссылка
        on_delete=models.CASCADE,
        related_name='medias'  # теперь user.reports.all() вернёт все отчёты
    )
    media_type = models.CharField()
    def __str__(self):
        return f"{self.media_type}"