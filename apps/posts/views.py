from django.shortcuts import render
from rest_framework import generics
from django.views.generic import ListView, DetailView
from .models import Post
from .serializers import PostSerializer


class PostListView(generics.ListCreateAPIView):
    """
    Post List View controller
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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
