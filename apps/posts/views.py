# Python Modules
from typing import Any

# Django Modules
from django.views.generic import ListView, DetailView
from django.db.models import QuerySet, Count
from django.shortcuts import redirect
from django.views.generic import CreateView

# Django Rest Framework Modules
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.response import Response

# Project Modules
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer
from apps.users.models import CustomUser


class PostCreateView(CreateView):
    model = Post
    fields = ['community', 'content', 'pinned', 'tags']
    template_name = 'posts/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        return redirect('post-page-detail', pk=post.pk)


class PostListView(generics.ListCreateAPIView):
    """
    Post List View controller
    """
    queryset = Post.objects.filter(deleted_at__isnull=True)
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(deleted_at__isnull=True)
        community = self.request.query_params.get('community', None)
        if community:
            queryset = queryset.filter(community=community)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Post Detail View controller
    """
    queryset = Post.objects.filter(deleted_at__isnull=True)
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class PostPageListView(ListView):
    """
    Post Page List View controller
    """
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20


class PostPageDetailView(DetailView):
    """
    Post Page Detail View
    """
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


class PostViewSet(ViewSet):
    """
        Creating Post ViewSet for handling Event-related endpoints
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        """ Optimized Queryset which have:
               - author
               - prefetch_related
               - select_related
               - annotate (likes_count and comments_count)
        """
        return(
            Post.objects
            .filter(deleted_at__isnull=True)
            .select_related('author')
            .prefetch_related('comments', 'likes')
            .annotate(
                likes_count=Count('likes', distinct=True),
                comments_count=Count('comments', distinct=True)
            )
        )


    def list(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            ** kwargs: dict[str, Any],
    ) -> DRFResponse:
        """ Creating GET request"""

        all_posts: QuerySet[Post] = self.get_queryset()

        serializer: PostSerializer = PostSerializer(
            all_posts,
            many=True,
            context={'request': request}
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
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
    permission_classes = [IsAuthenticated]

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        try:
            return (
                Post.objects
                .select_related('author')
                .prefetch_related('comments')
                .prefetch_related('replies__author')
                .get(id=post_id)
            )
        except Post.DoesNotExist:
            return None

    def list(self, request, post_id=None):
        post = self.get_post()
        if not post:
            return Response({'detail': 'Post not found'}, status=HTTP_404_NOT_FOUND)
        
        comments = (Comment.objects
                    .filter(post=post, parent__isnull=True)
                    .select_related('author')
                    .order_by('created_at'))

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, post_id=None):
        post = self.get_post()
        if not post:
            return Response({'detail': 'Post not found'}, status=HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем автора и пост автоматически
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LikeViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_post(self):
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

    def create(self, request, post_id=None):
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

    def destroy(self, request, post_id=None):
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
