# Python Modules
from typing import Any

# Django Modules
from django.views.generic import ListView, DetailView
from django.db.models import QuerySet, Count
from django.shortcuts import redirect

# Django Rest Framework Modules
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

# Project Modules
from .models import Post
from .serializers import PostSerializer
from .models import Post


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
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Post Detail View controller
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


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

    def list(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            ** kwargs: dict[str, Any],
    ) -> DRFResponse:
        """ Creating GET request"""

        all_posts: QuerySet[Post] = Post.objects.all()

        serializer: PostSerializer = PostSerializer(
            all_posts,
            many=True,
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
            data=request.data
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

        serializer.save()

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
            post: Post = Post.objects.get(pk=kwargs['pk'])
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
            post: Post = Post.objects.get(id=kwargs['id'])
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
            from apps.users.models import CustomUser
            target_user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return DRFResponse(
                data={'error': 'User not found'},
                status=HTTP_404_NOT_FOUND
            )
        
        user_posts = Post.objects.filter(author=target_user).order_by('-created_at')
        serializer = PostSerializer(user_posts, many=True)
        
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )