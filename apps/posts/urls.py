# Django Modules
from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# Project Modules
from .views import (
    PostViewSet,
    CommentViewSet,
    LikeViewSet,
)


router = DefaultRouter(trailing_slash=True)
router.register(r'api', PostViewSet, basename='post')

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

like_detail = LikeViewSet.as_view({
    'post': 'create',
    'delete': 'destroy',
})

urlpatterns = [
    # Comments
    path('<uuid:post_id>/comments/', comment_list, name='post-comments'),

    # Likes
    path('<uuid:post_id>/like/', like_detail, name='post-like'),
]

urlpatterns += router.urls