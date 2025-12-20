# Python modules
from typing import Any
from random import choice, randint, sample
from datetime import datetime

# Django modules
from django.core.management.base import BaseCommand

# Project modules
from apps.posts.models import Post, Comment, Tag, Like
from apps.users.models import CustomUser
from apps.communities.models import Community


class Command(BaseCommand):
    help = "Generate posts, comments tags and likes for testing"

    CONTENT_SAMPLES = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.",
        "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.",
        "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet.",
        "Consectetur, adipisci velit, sed quia non numquam eius modi tempora.",
        "Et harum quidem rerum facilis est et expedita distinctio.",
        "Nam libero tempore, cum soluta nobis est eligendi optio cumque.",
    ]

    TAG_NAMES = [
        "technology", "science", "art", "music", "sports",
        "travel", "food", "photography", "design", "coding",
        "python", "django", "javascript", "react", "webdev",
        "news", "politics", "health", "fitness", "education"
    ]

    def __generate_tags(self) -> list[Tag]:
        tags_before = Tag.objects.count()
        tag_objects = []
        for tag_name in self.TAG_NAMES:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)
        tags_after = Tag.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {tags_after - tags_before} tags.")
        )
        return tag_objects

    def __generate_posts(self, post_count: int = 500) -> list[Post]:
        users = list(CustomUser.objects.all())
        communities = list(Community.objects.all())
        tags = list(Tag.objects.all())
        
        if not users:
            self.stdout.write(self.style.ERROR("No users found. Create users first"))
            return []
        
        posts_before = Post.objects.count()
        created_posts = []
        
        for i in range(post_count):
            author = choice(users)
            community = choice(communities) if communities else None
            content = choice(self.CONTENT_SAMPLES) + f" Post #{i+1}"
            pinned = randint(0, 100) < 5
            
            post = Post.objects.create(
                author=author,
                community=community,
                content=content,
                pinned=pinned
            )
            
            if tags:
                post_tags = sample(tags, k=min(randint(0, 5), len(tags)))
                post.tags.set(post_tags)
            
            created_posts.append(post)
        
        posts_after = Post.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {posts_after - posts_before} posts.")
        )
        return created_posts

    def __generate_comments(self, comment_count: int = 1000) -> None:
        posts = list(Post.objects.all())
        users = list(CustomUser.objects.all())
        
        if not posts or not users:
            return
        
        comments_before = Comment.objects.count()
        created_comments = []
        
        for i in range(comment_count):
            post = choice(posts)
            author = choice(users)
            content = choice(self.CONTENT_SAMPLES) + f" Comment #{i+1}"
            
            parent = None
            if randint(0, 100) < 30 and post.comments.exists():
                existing_comments = list(post.comments.all())
                parent = choice(existing_comments)
            
            comment = Comment(
                post=post,
                author=author,
                parent=parent,
                content=content
            )
            created_comments.append(comment)
        
        Comment.objects.bulk_create(created_comments, ignore_conflicts=True)
        comments_after = Comment.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {comments_after - comments_before} comments.")
        )

    def __generate_likes(self, like_count: int = 2000) -> None:
        posts = list(Post.objects.all())
        users = list(CustomUser.objects.all())
        
        if not posts or not users:
            return
        
        likes_before = Like.objects.count()
        created_likes = []
        
        for i in range(like_count):
            post = choice(posts)
            user = choice(users)
            
            if not Like.objects.filter(post=post, user=user).exists():
                like = Like(post=post, user=user)
                created_likes.append(like)
        
        Like.objects.bulk_create(created_likes, ignore_conflicts=True)
        likes_after = Like.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {likes_after - likes_before} likes.")
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        start_time = datetime.now()
        
        self.__generate_tags()
        posts = self.__generate_posts(post_count=500)
        if posts:
            self.__generate_comments(comment_count=1000)
            self.__generate_likes(like_count=2000)