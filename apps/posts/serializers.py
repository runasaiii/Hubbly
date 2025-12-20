# Python modules
from typing import Any, Optional
from rest_framework.serializers import (
    ReadOnlyField, 
    SerializerMethodField,
    ModelSerializer,
    ListField,
    CharField,
    )

# Project modules
from .models import Post, Comment, Tag, Like


class TagSerializer(ModelSerializer):
    """Serializer for tag model"""
    
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class CommentSerializer(ModelSerializer):
    """Serializer for comment model with nested replies"""
    
    author_username: ReadOnlyField = ReadOnlyField(source='author.username')
    replies: SerializerMethodField = SerializerMethodField()

    class Meta: 
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'parent', 'content', 'created_at', 'replies']
        read_only_fields = ['id', 'created_at', 'author_username', 'replies','post', 'author']

    def get_replies(self, obj: Comment) -> list[dict[str, Any]]:
        """Get nested replies for a comment."""
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostSerializer(ModelSerializer):
    """Serializer for post model with info like tags, comments and likes"""
    
    author_username: ReadOnlyField = ReadOnlyField(source='author.username')
    community_name: SerializerMethodField = SerializerMethodField()
    tags: TagSerializer = TagSerializer(many=True, read_only=True)
    tags_list: ListField = ListField(
        child=CharField(max_length=50),
        write_only=True,
        required=False,
        allow_empty=True
    )
    comments_count: SerializerMethodField = SerializerMethodField()
    likes_count: SerializerMethodField = SerializerMethodField()
    is_liked: SerializerMethodField = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_username',
            'community',
            'community_name',
            'content',
            'pinned',
            'tags',
            'tags_list',
            'created_at',
            'comments_count',
            'likes_count',
            'is_liked',
        ]
        read_only_fields = ['id', 'created_at', 'author', 'comments_count', 'likes_count', 'is_liked']

    def get_community_name(self, obj: Post) -> Optional[str]:
        """Get community name if post belongs to community"""
        if obj.community:
            return obj.community.name
        return None

    def get_comments_count(self, obj: Post) -> int:
        """Get total number of comments on the post"""
        return obj.comments.count()

    def get_likes_count(self, obj: Post) -> int:
        """Get total number of likes on the post"""
        return obj.likes.count()

    def get_is_liked(self, obj: Post) -> bool:
        """Check if current user has liked the post"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def create(self, validated_data: dict[str, Any]) -> Post:
        """Create a new post with tags"""
        tags_list = validated_data.pop('tags_list', [])
        post = super().create(validated_data)
        
        if tags_list:
            tag_objects = []
            for tag_name in tags_list:
                tag_name = tag_name.strip().lower()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tag_objects.append(tag)
            post.tags.set(tag_objects)
        
        return post

    def update(self, instance: Post, validated_data: dict[str, Any]) -> Post:
        """Update post and its tags"""
        tags_list = validated_data.pop('tags_list', None)
        post = super().update(instance, validated_data)
        
        if tags_list is not None:
            tag_objects = []
            for tag_name in tags_list:
                tag_name = tag_name.strip().lower()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tag_objects.append(tag)
            post.tags.set(tag_objects)
        
        return post

