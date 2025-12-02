# Python modules
from typing import Any

# Django modules
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    UUIDField,
    DateField,
    DecimalField,
    DateTimeField
    )
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from django.db import models

#App modules
from apps.abstracts.models import AbstractBaseModel
from apps.users.validators import (
    validate_email_domain, 
    validate_username_no_special_chars
)


class CustomUserManager(BaseUserManager):
    """Custom User manager for data base requests"""
    
    def __obtain_user_instance(
            self,
            email: str,
            full_name: str,
            username: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Get user instance"""
        if not email:
            raise ValidationError(
                message="Email field is required",
                code="email_empty"
            )
        if not full_name:
            raise  ValidationError(
                message="Full name field is required",
                code="full_name_empty"
            )
        
        new_user: 'CustomUser'= self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            password=password,
            **kwargs,
        )
        return new_user
    
    def create_user(
            self,
            email: str,
            full_name: str,
            username: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create CustomUser"""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email=self.normalize_email(email),
            username=username,
            password=password,
            full_name=full_name,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user
    
    def create_superuser(
            self,
            email: str,
            full_name: str,
            username: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create Super User"""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """
    Custom User model ith common fields."""
    EMAIL_MAX_LENGTH = 150
    USERNAME_MAX_LENGTH = 30
    FULL_NAME_MAX_LENGTH = 100
    PASSWORD_MIN_LENGTH = 8
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MAX_LENGTH = 30
    CITY_MAX_LENGTH = 30
    COUNTRY_MAX_LENGTH = 30
    PHONE_MAX_LENGTH = 15


    first_name = CharField(
        max_length = FIRST_NAME_MAX_LENGTH,
        blank = True,
        verbose_name='first name',
        help_text='First name of the user.',
        )
    last_name = CharField(
        max_length = LAST_NAME_MAX_LENGTH,
        blank = True,
        verbose_name='last name',
        help_text='Last name of the user.',
        )
    full_name = CharField(
        max_length = FULL_NAME_MAX_LENGTH,
        blank = True,
        verbose_name='full name',
        help_text='Full name of the user.',
        )
    username = CharField(
        max_length = USERNAME_MAX_LENGTH, 
        unique = True,
        verbose_name='username',
        help_text='Required. 30 characters or fewer. Letters and digits only.',
        )
    email = EmailField(
        unique = True,
        max_length = EMAIL_MAX_LENGTH,
        db_index=True,
        validators = [validate_email_domain],
        verbose_name='email address',
        help_text='Required. Enter a valid email address.',
        )
    phone_number = CharField(
        max_length = PHONE_MAX_LENGTH,
        blank = True,
        verbose_name='phone number',
        help_text='Phone number of the user.',
        null=True,
        )
    city = CharField(
        max_length = CITY_MAX_LENGTH,
        blank = True,
        verbose_name='city',
        help_text='City of the user.',
        null=True,
        )
    country = CharField(
        max_length = COUNTRY_MAX_LENGTH,
        blank = True,
        verbose_name='country',
        help_text='Country of the user.',
        null=True,
        )
    birthdate = DateField(
        null=True,
        blank=True,
        verbose_name='birthdate',
        help_text='Birthdate of the user.',
    )
    is_active = BooleanField(
        default = True,
        verbose_name='active',
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
        )
    is_staff = BooleanField(
        default=False,
        verbose_name='staff status',
        help_text='Designates whether the user can log into this admin site.',
    )
    date_joined = DateTimeField(
        default=timezone.now,
        verbose_name='date joined',
        help_text='The date and time when the user joined.',
    )
    last_login = DateTimeField(
        null=True,
        blank=True,
        verbose_name='last login',
        help_text='The date and time of the user\'s last login.',
    )

    def __str__(self) -> str:
        return self.email
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']
    objects = CustomUserManager()

    class Meta():
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ('-created_at',)

    def clean(self) -> None:
        """ """
        validate_username_no_special_chars(
            username=self.username,
        )
        return super().clean()



class Profile(models.Model):
    """
    Profile model ith common fields.
    """
    MAX_LENGTH = 100
    GENDER_MAX_LENGTH = 10

    user = models.OneToOneField(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE, 
        related_name = 'profile'
    )
    display_name = models.CharField(
        max_length = MAX_LENGTH,
        blank = True
    )
    bio = models.TextField(
        blank = True
        )
    location = models.CharField(
        max_length = MAX_LENGTH,
        blank = True
    )
    interests = models.JSONField(
        default = list, 
        blank = True
    )
    is_verified = models.BooleanField(
        default = False
        )
    avatar = models.URLField(
        blank = True,
        null = True
    )
    gender = models.CharField(
        max_length = GENDER_MAX_LENGTH,
        blank = True,
        choices=[
            ('male','Male'),
            ('female','Female'),
            ('other','Other'),
        ],
        default = 'other'
    )
    updated_at = models.DateTimeField(
        auto_now = True
    )

    def __str__(self):
        return self.display_name or self.user.email


class Media(AbstractBaseModel):
    """
    Media model ith common fields.
    """
    MEDIA_TYPE_MAX_LENGTH = 20
    TITLE_MAX_LENGTH = 100


    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('file', 'File'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medias'
    )
    media_type = models.CharField(
        max_length=MEDIA_TYPE_MAX_LENGTH,
        choices=MEDIA_TYPES,
        default='image'
    )
    file = models.FileField(
        upload_to='media_files/',
        blank=False,
        null=False
    )
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        blank=True
    )
    description = models.TextField(
        blank=True
    )

    def __str__(self) -> str:
        return f"{self.media_type}: {self.title or self.file.name}"