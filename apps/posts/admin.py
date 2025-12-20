# Unfold Modules
from unfold.admin import ModelAdmin

# Django modules
from django.contrib.admin import register

# Project modules
from .models import (
    Post,
    Comment,
    Tag,
    Report,
    Like,
)


@register(Post)
class PostAdmin(ModelAdmin):
    """
    ModelAdmin for PostAdmin
    """
    list_display = ('id', 'author', 'community', 'pinned', 'created_at')
    list_filter = ('pinned', 'community')
    search_fields = ('author__email', 'author__username', 'content')
    date_hierarchy = 'created_at'


@register(Comment)
class CommentAdmin(ModelAdmin):
    """
    ModelAdmin for CommentAdmin
    """
    list_display = ('id', 'post', 'author', 'parent', 'created_at')
    search_fields = ('author__email', 'author__username', 'content')
    date_hierarchy = 'created_at'


@register(Tag)
class TagAdmin(ModelAdmin):
    """
    ModelAdmin for TagAdmin
    """
    list_display = ('id', 'name')
    search_fields = ('name',)


@register(Report)
class ReportAdmin(ModelAdmin):
    """
    ModelAdmin for ReportAdmin
    """
    ...
    # backlog poka


@register(Like)
class LikeAdmin(ModelAdmin):
    """
    ModelAdmin for LikeAdmin
    """
    list_display = ('id', 'post', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'user__username', 'post__content')
    date_hierarchy = 'created_at'