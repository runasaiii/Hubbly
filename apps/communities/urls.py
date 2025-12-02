# Django Modules
from django.urls import path, include

# Project Modules
from .views import (
    CommunityListView,
    CommunityDetailView,
    CommunityPageListView,
    CommunityPageDetailView,
    CommunityViewSet,
)

# DRF
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', CommunityViewSet, basename='community')

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


