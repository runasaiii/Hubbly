# Django Modules
from django.urls import path, include

# Project Modules
from .views import (
    EventViewSet,
)

# Rest Framework Modules
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    # rest apishki
    path('api/', include(router.urls)),
]


