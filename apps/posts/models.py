from django.db import models
import uuid
from apps.users.models import User  
from apps.communities.models import Community
from apps.abstracts.models import AbstractBaseModule

class Tag(models.Model):
    MAX_LENGTH = 50
    id = models.UUIDField(
        primary_key = True, 
        default = uuid.uuid4, 
        editable = False
    )
    name = models.CharField(
        max_length = MAX_LENGTH, 
        unique = True
    )

    def __str__(self):
        return self.name


class Post(AbstractBaseModule):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    author = models.ForeignKey(
        to = User, 
        on_delete = models.CASCADE, 
        related_name = 'posts'
    )
    community = models.ForeignKey(
        to = Community,
        on_delete = models.CASCADE,
        related_name = 'posts',
        null = True,
        blank = True
    )
    content = models.TextField()
    pinned = models.BooleanField(default = False)
    tags = models.ManyToManyField(
        to = Tag,
        related_name = 'posts',
        blank = True
    )

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
    

class Comment(AbstractBaseModule):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    post = models.ForeignKey(
        to = Post, 
        on_delete = models.CASCADE, 
        related_name = 'comments'
    )
    author = models.ForeignKey(
        to = User, 
        on_delete = models.CASCADE
    )
    parent = models.ForeignKey(
        to = 'self', 
        on_delete = models.CASCADE, 
        related_name = 'replies', 
        null = True, 
        blank = True
    )
    content = models.TextField()


    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.id}"