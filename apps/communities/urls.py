from django.urls import path
from .views import (
    CommunityListView, CommunityDetailView,
    CommunityPageListView, CommunityPageDetailView,
)


urlpatterns = [
    # HTML pages (default)
    path('', CommunityPageListView.as_view(), name='community-page-list'),
    path('<uuid:pk>/', CommunityPageDetailView.as_view(), name='community-page-detail'),
    # Back-compat aliases
    path('page/', CommunityPageListView.as_view(), name='community-page-list-legacy'),
    path('page/<uuid:pk>/', CommunityPageDetailView.as_view(), name='community-page-detail-legacy'),

    # REST API
    path('api/', CommunityListView.as_view(), name='community-list'),
    path('api/<uuid:pk>/', CommunityDetailView.as_view(), name='community-detail'),
]


