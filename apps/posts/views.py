# Python Modules
from typing import Any

# Django Modules
from django.db.models import QuerySet, Count

# Django Rest Framework Modules
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)
from rest_framework.response import Response

# Project Modules
from .models import Post, Like, Comment
from .serializers import (
    PostSerializer,
    PostNotFoundSerializer,
    PostResponseSerializer,
    CommentSerializer,
    CommentNotFoundSerializer,
    CommentResponseSerializer,
)
from .filters import PostFilter
from apps.users.models import CustomUser
from .permissions import IsPostAuthor

# Swagger modules
from drf_spectacular.utils import extend_schema, OpenApiResponse


class PostViewSet(ViewSet):
    """ViewSet for handling post related endpoints"""
    
    def get_permissions(self):
        if self.action in ('partial_update', 'destroy'):
            permission_classes = (IsAuthenticated, IsPostAuthor)
        else:
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]

    filterset_class = PostFilter

    def get_queryset(self) -> QuerySet[Post]:
        """Get optimized queryset with author, comments, likes and annotations"""
        return (
            Post.objects
            .filter(deleted_at__isnull=True)
            .select_related('author', 'community')
            .prefetch_related('comments', 'likes', 'tags')
            .annotate(
                likes_count=Count('likes', distinct=True),
                comments_count=Count('comments', distinct=True)
            )
        )


    @extend_schema(
        summary="List all posts",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Returns list of top-level posts",
                response=PostSerializer,
            )
        }
    )
    def list(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get list of posts with filtering"""
        queryset = self.get_queryset()
        
        filterset = self.filterset_class(request.query_params, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        
        ordering = request.query_params.get('ordering', '-pinned,-created_at')
        if ordering:
            queryset = queryset.order_by(*ordering.split(','))

        serializer: PostSerializer = PostSerializer(
            queryset,
            many=True,
            context={'request': request}
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )


    @extend_schema(
        summary="Create a Post",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Posts successfully created",
                response=PostSerializer,
            ),
        }
    )
    def create(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """ Creating POST request"""

        serializer: PostSerializer = PostSerializer(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

        serializer.save(author=request.user)

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED,
        )


    @extend_schema(
        summary="Retrieve a single post by ID",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successfully returns the requested post",
                response=PostSerializer,
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Event with this ID does not exist",
                response=PostNotFoundSerializer,
            )
        }
    )
    def retrieve(
            self,
            request: DRFRequest,
            pk: str | None = None,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get single post by ID"""
        try:
            post = self.get_queryset().get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return DRFResponse(serializer.data, status=HTTP_200_OK)
        except Post.DoesNotExist:
            return DRFResponse({'detail': 'Post not found'}, status=HTTP_404_NOT_FOUND)


    @extend_schema(
        summary="Partially update a post",
        request=PostSerializer,
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Post successfully updated",
                response=PostSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data",
                response= PostResponseSerializer,
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Post with this ID does not exist",
                response=PostNotFoundSerializer,
            ),
        }
    )
    def partial_update(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """ Creating PATCH request"""

        try:
            post: Post = self.get_queryset().get(pk=kwargs['pk'])
        except Post.DoesNotExist:
            return DRFResponse(
                data={
                    'pk': [f"Post with that id={kwargs['pk']} does not exists"]
                },
                status=HTTP_404_NOT_FOUND
            )

        serializer: PostSerializer = PostSerializer(
            data=request.data,
            instance=post,
            partial=True,
            context={'request': request}
        )

        serializer.is_valid()

        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK,
        )


    @extend_schema(
        summary="Delete a post",
        responses={
            HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Post successfully deleted"
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Post with this ID does not exist",
                response=PostNotFoundSerializer,
            ),
        }
    )
    def destroy(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """ Creating DELETE request"""

        try:
            post: Post = self.get_queryset().get(id=kwargs['id'])
        except Post.DoesNotExist:
            return DRFResponse(
                data={
                    f"Post with that id={kwargs['pk']} does not exists"
                },
                status=HTTP_404_NOT_FOUND
            )

        post.delete()

        return DRFResponse(
            status=HTTP_204_NO_CONTENT
        )


    @extend_schema(
        summary="Get All User's Posts",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Returns list of top-level posts",
                response=PostSerializer,
            )
        }
    )
    @action(
        methods=('GET',),
        detail=False,
        url_path='user/(?P<user_id>[^/.]+)',
        url_name='user_posts',
        permission_classes = (IsAuthenticated,),
    )
    def get_user_posts(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """Get posts by specific user"""
        user_id = kwargs.get('user_id')
        try:
            target_user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return DRFResponse(
                data={'error': 'User not found'},
                status=HTTP_404_NOT_FOUND
            )
        
        user_posts = (self.get_queryset()
                      .filter(author=target_user, deleted_at__isnull=True)
                      .order_by('-created_at'))

        serializer = PostSerializer(user_posts, many=True, context={'request': request})
        
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )


class CommentViewSet(ViewSet):
    """ViewSet for handling comment related endpoints"""
    
    permission_classes = [IsAuthenticated]

    def get_post(self) -> Post | None:
        """Get post by ID from kwargs."""
        post_id = self.kwargs.get('post_id')
        try:
            return (
                Post.objects
                .select_related('author')
                .prefetch_related('comments__author', 'comments__replies__author')
                .get(id=post_id)
            )
        except Post.DoesNotExist:
            return None

    @extend_schema(
        summary="List comments for a post",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Returns list of top-level comments for a post",
                response=CommentSerializer(many=True)
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Post not found",
                response=CommentNotFoundSerializer,
            ),
        }
    )
    def list(
        self,
        request: DRFRequest,
        post_id: str | None = None
    ) -> DRFResponse:
        """Get all comments for a specific post."""
        post = self.get_post()
        if not post:
            return Response({'detail': 'Post not found'}, status=HTTP_404_NOT_FOUND)
        
        comments = (
            Comment.objects
            .filter(post=post, parent__isnull=True)
            .select_related('author')
            .order_by('created_at')
        )

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


    @extend_schema(
        summary="Create a comment on a post",
        request=CommentSerializer,
        responses={
            HTTP_201_CREATED: OpenApiResponse(
                description="Successfully created comment",
                response=CommentSerializer
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Validation error",
                response=CommentResponseSerializer,

            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Post not found",
                response=CommentNotFoundSerializer,
            ),
        }
    )
    def create(
        self,
        request: DRFRequest,
        post_id: str | None = None
    ) -> DRFResponse:
        """Create a new comment for a post"""
        post = self.get_post()
        if not post:
            return Response({'detail': 'Post not found'}, status=HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LikeViewSet(ViewSet):
    """ViewSet for handling like related endpoints"""
    
    permission_classes = [IsAuthenticated]

    def get_post(self) -> Post | None:
        """Get post by ID from kwargs."""
        post_id = self.kwargs.get('post_id')
        try:
            return (
                Post.objects
                .select_related('author')
                .prefetch_related('likes')
                .get(id=post_id)
            )
        except Post.DoesNotExist:
            return None


    @extend_schema(
        summary="Like a post",
        responses={
            HTTP_201_CREATED: OpenApiResponse(
                description="Post successfully liked",
                response=PostSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Post already liked",
                 response=PostResponseSerializer,
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Post not found",
                response=PostNotFoundSerializer,
            ),
        }
    )
    def create(
        self,
        request: DRFRequest,
        post_id: str | None = None
    ) -> DRFResponse:
        """Like a post"""
        post = self.get_post()
        if not post:
            return Response({'detail': 'Post not found'}, status=HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(
            post=post,
            user=request.user
        )

        if not created:
            return Response({'detail': 'Post already liked'}, status=HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=HTTP_201_CREATED)


    @extend_schema(
        summary="Unlike a post",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Post successfully unliked",
                response=PostSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Post was not liked",
                response=PostResponseSerializer,
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Post not found",
                response=PostNotFoundSerializer,
            ),
        }
    )
    def destroy(
        self,
        request: DRFRequest,
        post_id: str | None = None
    ) -> DRFResponse:
        """Unlike a post"""
        post = self.get_post()
        if not post:
            return Response({'detail': 'Post not found'}, status=HTTP_404_NOT_FOUND)

        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status=HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'detail': 'Post not liked'}, status=HTTP_400_BAD_REQUEST)
