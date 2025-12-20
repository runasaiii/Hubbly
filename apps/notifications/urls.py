# Django modules
from django.urls import path
from rest_framework.routers import DefaultRouter

# Project modules
from .views import NotificationListView, NotificationViewSet


router = DefaultRouter()
router.register(r'api', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
] + router.urls


