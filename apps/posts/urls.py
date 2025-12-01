from django.urls import path
from rest_framework.routers import DefaultRouter
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
    # HTML pages
    path('', PostPageListView.as_view(), name='post-page-list'),
    path('<uuid:pk>/', PostPageDetailView.as_view(), name='post-page-detail'),
    path('create/', PostCreateView.as_view(), name='post-page-create'),

    # Back-compat aliases
    path('page/', PostPageListView.as_view(), name='post-page-list-legacy'),
    path('page/<uuid:pk>/', PostPageDetailView.as_view(), name='post-page-detail-legacy'),

    # Comments linked to the post
    path('<uuid:post_id>/comments/', comment_list, name='post-comments'),

    # Likes linked to a post
    path('<uuid:post_id>/like/', like_detail, name='post-like'),

    # REST API постов
    path('api/', PostListView.as_view(), name='post-list'),
    path('api/<uuid:pk>/', PostDetailView.as_view(), name='post-detail'),
]

# Добавляем рутер только для PostViewSet
urlpatterns += router.urls