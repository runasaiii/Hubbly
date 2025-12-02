# Django Modules
from django.urls import path

# DRF
from rest_framework.routers import DefaultRouter

# Project Modules
from .views import PostViewSet, CommentViewSet, LikeViewSet, PostPageListView, PostPageDetailView, PostCreateView, PostListView, PostDetailView


router = DefaultRouter(trailing_slash=False)
router.register(r'v1', PostViewSet, basename='post')

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

like_detail = LikeViewSet.as_view({
    'post': 'create',
    'delete': 'destroy',
})

urlpatterns = [
    path('', PostPageListView.as_view(), name='post-page-list'),
    path('<uuid:pk>/', PostPageDetailView.as_view(), name='post-page-detail'),
    path('create/', PostCreateView.as_view(), name='post-page-create'),

    path('page/', PostPageListView.as_view(), name='post-page-list-legacy'),
    path('page/<uuid:pk>/', PostPageDetailView.as_view(), name='post-page-detail-legacy'),

    path('<uuid:post_id>/comments/', comment_list, name='post-comments'),

    path('<uuid:post_id>/like/', like_detail, name='post-like'),

    path('api/', PostListView.as_view(), name='post-list'),
    path('api/<uuid:pk>/', PostDetailView.as_view(), name='post-detail'),
]

urlpatterns += router.urls