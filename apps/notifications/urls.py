# Django modules
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Project modules
from .views import NotificationViewSet


router = DefaultRouter()
router.register(r'api', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
] + router.urls


