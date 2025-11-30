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
    replies = serializers.SerializerMethodField()

    class Meta: 
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'parent', 'content', 'created_at', 'replies']
        read_only_fields = ['id', 'created_at', 'author_username', 'replies','post', 'author']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    community_slug = serializers.ReadOnlyField(source='community.slug')
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()  # ← добавляем поле

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
            'comments_count', 
        ]
        read_only_fields = ['id', 'created_at', 'author', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()

