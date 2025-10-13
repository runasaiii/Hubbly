from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model"""
    class Meta:
        model = User
        fields = [
            'id',
            'username', 
            'email',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users"""
    class Meta:
        model = User
        fields = [
            'username',
            'email', 
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
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


class UserWithProfileSerializer(serializers.ModelSerializer):
    """Serializer for user model with nested profile"""
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
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


class ProfileUpdateSerializer(serializers.ModelSerializer):
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