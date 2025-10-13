from rest_framework import serializers
from .models import Community, CommunityMembership


class CommunitySerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

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
        ]
        read_only_fields = ['id', 'created_at']


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


