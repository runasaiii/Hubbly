# Django Rest modules
from typing import Any, Optional
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    Serializer,
    CharField,
    EmailField,
    IntegerField,
    ListField,
    ModelSerializer
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Django modules
from django.contrib.auth.password_validation import validate_password

# Project modules
from .models import CustomUser, Profile


class UserSerializer(ModelSerializer):
    """Serializer for user model"""
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username', 
            'email',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(ModelSerializer):
    """Serializer for creating new users"""
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'full_name',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'full_name': {'required': False, 'allow_blank': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')

        # Provide default full_name if not provided
        if 'full_name' not in validated_data or not validated_data.get('full_name'):
            validated_data['full_name'] = validated_data.get('username', '')
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class ProfileSerializer(ModelSerializer):
    """Serializer for profile model"""
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'display_name',
            'bio',
            'location', 
            'interests',
            'is_verified',
            'avatar'
        ]
        read_only_fields = ['id', 'user']


class UserWithProfileSerializer(ModelSerializer):
    """Serializer for user model with nested profile"""
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email', 
            'is_active',
            'created_at',
            'updated_at',
            'profile'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProfileUpdateSerializer(ModelSerializer):
    """Serializer for updating profile information"""
    class Meta:
        model = Profile
        fields = [
            'display_name',
            'bio',
            'location',
            'interests', 
            'avatar'
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to include user data in JWT token response"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['full_name'] = user.full_name
        token['email'] = user.email
        return token
    

class RegistrationSerializer(Serializer):
    """Serializer for user registration"""

    password = CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password]
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'full_name',
            'password'
        ]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


# Saya's code for Login
class UserLoginSerializer(Serializer):
    """ Serializer for user login. """
    email = EmailField(
        required=True,
        max_length=CustomUser.EMAIL_MAX_LENGTH,
    )
    password = CharField(
        required=True,
        min_length=CustomUser.PASSWORD_MIN_LENGTH,
    )
    class Meta:
        """Customization of the Serializer metadata."""

        fields = {
            'email',
            'password',
        }

    def validate_email(self, value: str,) -> str:
        """ Validates the email field """
        return value.lower()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """ Validates the input data """
        email: str = attrs['email']
        password: str = attrs['password']

        user: Optional[CustomUser] = CustomUser.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                detail={
                    'email': [f'User with that email {email} does not exists']
                }
            )
        if not user.check_password(raw_password=password):
            raise ValidationError(
                detail={
                    'password': ['Incorrect password']
                }
            )
        attrs['user'] = user
        return super().validate(attrs)