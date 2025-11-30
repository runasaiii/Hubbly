from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostListView, 
    PostDetailView,
    PostPageListView, 
    PostPageDetailView,
    PostCreateView,
    PostViewSet,
)

router = DefaultRouter(trailing_slash=False)
router.register(prefix='v1', viewset=PostViewSet, basename='post')

urlpatterns = [
    # HTML pages (default)
    path('', PostPageListView.as_view(), name='post-page-list'),
    path('<uuid:pk>/', PostPageDetailView.as_view(), name='post-page-detail'),

    # New: page for creating posts
    path('create/', PostCreateView.as_view(), name='post-page-create'),

    # Back-compat aliases
    path('page/', PostPageListView.as_view(), name='post-page-list-legacy'),
    path('page/<uuid:pk>/', PostPageDetailView.as_view(), name='post-page-detail-legacy'),

    # REST API
    path('api/', PostListView.as_view(), name='post-list'),
    path('api/<uuid:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('', include(router.urls)),
]
