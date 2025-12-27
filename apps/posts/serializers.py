# Python modules
from typing import Any, Optional
from rest_framework.serializers import (
    ReadOnlyField, 
    SerializerMethodField,
    Serializer,
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


class CommentNotFoundSerializer(Serializer):
    """
        Serializer for HTTP 404 Method Not Allowed response.
    """
    detail = CharField()

    class Meta:
        """Customization of the Serializer metadata."""
        fields = (
            "detail",
        )


class CommentResponseSerializer(Serializer):
    """
        Serializer for comment errors.
    """
    author_username = ListField(
        child=CharField(),
        required=False,
    )
    parent = ListField(
        child=CharField(),
        required=False,
    )

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "parent",
            "author_username",
        )


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
    liked_by: SerializerMethodField = SerializerMethodField()
    comment_authors: SerializerMethodField = SerializerMethodField()
    can_edit: SerializerMethodField = SerializerMethodField()
    is_author: SerializerMethodField = SerializerMethodField()

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
            'edited_at',
            'comments_count',
            'likes_count',
            'is_liked',
            'liked_by',
            'comment_authors',
            'can_edit',
            'is_author',
        ]
        read_only_fields = ['id', 'created_at', 'edited_at', 'author', 'comments_count', 'likes_count', 'is_liked', 'liked_by', 'comment_authors', 'can_edit', 'is_author']

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

    def get_liked_by(self, obj: Post) -> list[dict[str, Any]]:
        """Get list of users who liked the post"""
        likes = obj.likes.select_related('user').all()[:10]  # Limit to first 10
        return [
            {
                'id': str(like.user.id),
                'username': like.user.username,
            }
            for like in likes
        ]

    def get_comment_authors(self, obj: Post) -> list[dict[str, Any]]:
        """Get list of unique users who commented on the post"""
        comments = obj.comments.select_related('author').all()
        authors_dict = {}
        for comment in comments:
            author_id = str(comment.author.id)
            if author_id not in authors_dict:
                authors_dict[author_id] = {
                    'id': author_id,
                    'username': comment.author.username,
                }
                if len(authors_dict) >= 10:  # Limit to first 10 unique authors
                    break
        return list(authors_dict.values())

    def get_can_edit(self, obj: Post) -> bool:
        """Check if current user can edit this post"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        # Only author can edit
        if obj.author != request.user:
            return False
        # Check time limit
        return obj.can_be_edited()

    def get_is_author(self, obj: Post) -> bool:
        """Check if current user is the author"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.author == request.user

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


class PostNotFoundSerializer(Serializer):
    """
        Serializer for HTTP 404 Method Not Allowed response.
    """
    detail = CharField()

    class Meta:
        """Customization of the Serializer metadata."""
        fields = (
            "detail",
        )


class PostResponseSerializer(Serializer):
    """
        Serializer for comment errors.
    """
    author_username = ListField(
        child=CharField(),
        required=False,
    )
    community_name = ListField(
        child=CharField(),
        required=False,
    )

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "community_name",
            "author_username",
        )

