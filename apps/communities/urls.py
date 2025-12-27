# Django Modules
from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# Project Modules
from .views import (
    CommunityViewSet,
)


router = DefaultRouter()
router.register(r'api', CommunityViewSet, basename='community')

urlpatterns = [
    path('', include(router.urls)),
]


