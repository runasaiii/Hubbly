# Python modules
from rest_framework import serializers

# Project modules
from .models import Post, Comment, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'author_username',
            'parent',
            'content',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    community_slug = serializers.ReadOnlyField(source='community.slug')
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_username',
            'community',
            'community_slug',
            'content',
            'pinned',
            'tags',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'author']


