from django.contrib.admin import register
from unfold.admin import ModelAdmin
from .models import (
    Post,
    Comment,
    Tag,
    Report,
    Like,
)

#register Post App
@register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('id', 'author', 'community', 'pinned', 'created_at')
    list_filter = ('pinned', 'community')
    search_fields = ('author__email', 'author__username', 'content')
    date_hierarchy = 'created_at'

#register Comment App
@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('id', 'post', 'author', 'parent', 'created_at')
    search_fields = ('author__email', 'author__username', 'content')
    date_hierarchy = 'created_at'

#register Tag App
@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

#register Report App
@register(Report)
class ReportAdmin(ModelAdmin):
    ...

#register Like App
@register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ('id', 'post', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'user__username', 'post__content')
    date_hierarchy = 'created_at'

# Register your models here.
