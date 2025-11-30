from django.urls import path
from .views import (
    PostListView, 
    PostDetailView,
    PostPageListView, 
    PostPageDetailView,
    PostCreateView,
)


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
]
