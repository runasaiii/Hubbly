from rest_framework import serializers
from .models import Community, CommunityMembership


class CommunitySerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    membership_role = serializers.SerializerMethodField()
    membership_status = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = [
            'id',
            'name',
            'slug',
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
        read_only_fields = ['id', 'created_at', 'is_owner', 'is_member', 'membership_role', 'membership_status']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.owner == request.user
        return False

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.memberships.filter(user=request.user, status='active').exists()
        return False

    def get_membership_role(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = obj.memberships.filter(user=request.user).first()
            if membership:
                return membership.role
        return None

    def get_membership_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = obj.memberships.filter(user=request.user).first()
            if membership:
                return membership.status
        return None


class CommunityMembershipSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    community_name = serializers.ReadOnlyField(source='community.name')

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


