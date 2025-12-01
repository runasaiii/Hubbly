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
    list_display = ('id', 'author', 'community', 'pinned', 'created_at')
    list_filter = ('pinned', 'community')
    search_fields = ('author__email', 'author__username', 'content')
    date_hierarchy = 'created_at'

@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('id', 'post', 'author', 'parent', 'created_at')
    search_fields = ('author__email', 'author__username', 'content')
    date_hierarchy = 'created_at'

@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@register(Report)
class ReportAdmin(ModelAdmin):
    ...

@register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ('id', 'post', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'user__username', 'post__content')
    date_hierarchy = 'created_at'