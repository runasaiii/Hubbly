from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Post, Comment, Tag


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('id', 'author', 'community', 'pinned', 'created_at')
    list_filter = ('pinned', 'community')
    search_fields = ('author__email', 'author__username', 'content')
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('id', 'post', 'author', 'parent', 'created_at')
    search_fields = ('author__email', 'author__username', 'content')
    date_hierarchy = 'created_at'


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Register your models here.
