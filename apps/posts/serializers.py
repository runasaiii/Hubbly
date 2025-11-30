# Python modules
from rest_framework import serializers

# Project modules
from .models import Post, Comment, Tag, Like


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
    community_slug = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

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
            'likes_count',
            'is_liked',
        ]
        read_only_fields = ['id', 'created_at', 'author', 'comments_count', 'likes_count', 'is_liked']

    def get_community_slug(self, obj):
        if obj.community:
            return obj.community.slug
        return None

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

