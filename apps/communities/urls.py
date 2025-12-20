# Django Modules
from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# Project Modules
from .views import (
    CommunityListView,
    CommunityDetailView,
    CommunityPageListView,
    CommunityPageDetailView,
    CommunityViewSet,
)


router = DefaultRouter()
router.register(r'', CommunityViewSet, basename='community')

urlpatterns = [
    path('', CommunityPageListView.as_view(), name='community-page-list'),
    path('<uuid:pk>/', CommunityPageDetailView.as_view(), name='community-page-detail'),

    path('page/', CommunityPageListView.as_view(), name='community-page-list-legacy'),
    path('page/<uuid:pk>/', CommunityPageDetailView.as_view(), name='community-page-detail-legacy'),

    # rest api
    path('api/', CommunityListView.as_view(), name='community-list'),
    path('api/<uuid:pk>/', CommunityDetailView.as_view(), name='community-detail'),
]


