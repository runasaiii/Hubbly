# Python modules
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
    """
    ModelSerializer for TagSerializer
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class CommentSerializer(ModelSerializer):
    """
    ModelSerializer for CommentSerializer
    """
    author_username = ReadOnlyField(source='author.username')
    replies = SerializerMethodField()

    class Meta: 
        model: Comment = Comment
        fields = ['id', 'post', 'author', 'author_username', 'parent', 'content', 'created_at', 'replies']
        read_only_fields = ['id', 'created_at', 'author_username', 'replies','post', 'author']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostSerializer(ModelSerializer):
    """
    ModelSerializer for PostSerializer
    """
    author_username = ReadOnlyField(source='author.username')
    community_slug = SerializerMethodField()
    community_name = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    tags_list = ListField(
        child=CharField(max_length=50),
        write_only=True,
        required=False,
        allow_empty=True
    )
    comments_count = SerializerMethodField()
    likes_count = SerializerMethodField()
    is_liked = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_username',
            'community',
            'community_slug',
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

    def get_community_slug(self, obj):
        if obj.community:
            return obj.community.slug
        return None

    def get_community_name(self, obj):
        if obj.community:
            return obj.community.name
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

    def create(self, validated_data):
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

    def update(self, instance, validated_data):
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

