# Python modules
from typing import Any, Optional

# DRF modules
from rest_framework import serializers

# Project modules
from .models import Community, CommunityMembership


class CommunitySerializer(serializers.ModelSerializer):
    """Serializer for Community model with membership information"""
    
    owner: serializers.HiddenField = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_username: serializers.ReadOnlyField = serializers.ReadOnlyField(source='owner.username')
    is_owner: serializers.SerializerMethodField = serializers.SerializerMethodField()
    is_member: serializers.SerializerMethodField = serializers.SerializerMethodField()
    membership_role: serializers.SerializerMethodField = serializers.SerializerMethodField()
    membership_status: serializers.SerializerMethodField = serializers.SerializerMethodField()

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
        ]
        read_only_fields = [
            'id',
            'created_at',
            'owner_username',
            'is_owner',
            'is_member',
            'membership_role',
            'membership_status',
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


