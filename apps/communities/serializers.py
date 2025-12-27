# Python modules
from typing import Any, Optional

# DRF modules
from rest_framework import serializers
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    ListField,
)

# Project modules
from .models import Community, CommunityMembership


class CommunitySerializer(ModelSerializer):
    """Serializer for Community model with membership information"""
    
    owner = serializers.SerializerMethodField()
    owner_username: serializers.ReadOnlyField = serializers.ReadOnlyField(source='owner.username')
    is_owner: serializers.SerializerMethodField = serializers.SerializerMethodField()
    is_member: serializers.SerializerMethodField = serializers.SerializerMethodField()
    membership_role: serializers.SerializerMethodField = serializers.SerializerMethodField()
    membership_status: serializers.SerializerMethodField = serializers.SerializerMethodField()
    posts_count: serializers.SerializerMethodField = serializers.SerializerMethodField()
    members_count: serializers.SerializerMethodField = serializers.SerializerMethodField()
    slug: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = [
            'id',
            'name',
            'description',
            'visibility',
            'owner',
            'owner_username',
            'created_at',
            'is_owner',
            'is_member',
            'membership_role',
            'membership_status',
            'posts_count',
            'members_count',
            'slug',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'owner',
            'owner_username',
            'is_owner',
            'is_member',
            'membership_role',
            'membership_status',
            'posts_count',
            'members_count',
            'slug',
        ]

    def get_is_owner(self, obj: Community) -> bool:
        """Check if current user is owner of the community"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.owner == request.user
        return False

    def get_is_member(self, obj: Community) -> bool:
        """Check if current user is active member of the community"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.memberships.filter(user=request.user, status='active').exists()
        return False

    def get_membership_role(self, obj: Community) -> Optional[str]:
        """Get current users role in community"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = obj.memberships.filter(user=request.user).first()
            if membership:
                return membership.role
        return None

    def get_membership_status(self, obj: Community) -> Optional[str]:
        """Get current users membership status in community"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = obj.memberships.filter(user=request.user).first()
            if membership:
                return membership.status
        return None

    def get_posts_count(self, obj: Community) -> int:
        """Get total number of posts in the community"""
        if hasattr(obj, 'posts_count'):
            return obj.posts_count
        return obj.posts.count()

    def get_members_count(self, obj: Community) -> int:
        """Get total number of active members in the community (including owner)"""
        if hasattr(obj, 'active_members_count'):
            return 1 + (obj.active_members_count or 0)
        active_members = obj.memberships.filter(status='active').count()
        return 1 + active_members

    def get_slug(self, obj: Community) -> str:
        """Get slug for the community (using id as slug)"""
        return str(obj.id)

    def get_owner(self, obj: Community) -> str:
        """Get owner ID as string"""
        return str(obj.owner.id)


class NotFoundSerializer(Serializer):
    """
    Serializer for HTTP 404 Method Not Allowed response.
    """

    detail = CharField()

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "detail",
        )


class CommunityMembershipSerializer(serializers.ModelSerializer):
    """Serializer for CommunityMembership model"""
    
    user_username: serializers.ReadOnlyField = serializers.ReadOnlyField(source='user.username')
    community_name: serializers.ReadOnlyField = serializers.ReadOnlyField(source='community.name')

    class Meta:
        model = CommunityMembership
        fields = [
            'id',
            'user',
            'user_username',
            'community',
            'community_name',
            'role',
            'status',
            'joined_at',
        ]
        read_only_fields = ['id', 'joined_at']


class CommunityResponseSerializer(Serializer):
    """
    Serializer for community errors.
    """

    title = ListField(
        child=CharField(),
        required=False,
    )
    organizer_username = ListField(
        child=CharField(),
        required=False,
    )

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "organizer_username",
            "title",
        )