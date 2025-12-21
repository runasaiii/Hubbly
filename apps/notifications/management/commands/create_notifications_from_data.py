# Python modules
from typing import Any
from django.core.management.base import BaseCommand

# Project modules
from apps.notifications.models import Notification
from apps.posts.models import Like, Comment, Post
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Create notifications from existing likes and comments"

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Create notifications from existing data"""
        
        likes = Like.objects.select_related('post__author', 'user').all()
        likes_count = 0
        
        for like in likes:
            if like.post.author.id != like.user.id:
                exists = Notification.objects.filter(
                    user=like.post.author,
                    type='like',
                    related_object_id=like.post.id,
                    related_object_type='post',
                    message__contains=like.user.username
                ).exists()
                
                if not exists:
                    Notification.objects.create(
                        user=like.post.author,
                        type='like',
                        title='Ваш пост лайкнули',
                        message=f'{like.user.username} поставил(а) лайк вашему посту',
                        link=f'/posts/{like.post.id}',
                        related_object_id=like.post.id,
                        related_object_type='post',
                        is_read=False,
                    )
                    likes_count += 1
        
        
        comments = Comment.objects.select_related('post__author', 'author').all()
        comments_count = 0
        
        for comment in comments:
            if comment.post.author.id != comment.author.id:
                exists = Notification.objects.filter(
                    user=comment.post.author,
                    type='comment',
                    related_object_id=comment.post.id,
                    related_object_type='post',
                    message__contains=comment.author.username
                ).exists()
                
                if not exists:
                    Notification.objects.create(
                        user=comment.post.author,
                        type='comment',
                        title='Новый комментарий',
                        message=f'{comment.author.username} оставил(а) комментарий к вашему посту: {comment.content[:50]}{"..." if len(comment.content) > 50 else ""}',
                        link=f'/posts/{comment.post.id}',
                        related_object_id=comment.post.id,
                        related_object_type='post',
                        is_read=False,
                    )
                    comments_count += 1
    

