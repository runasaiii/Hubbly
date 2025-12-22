# Django modules
from django.urls import path, include

# DRF modules
from rest_framework.routers import DefaultRouter

# Project modules
from .views import (
    user_list,
    user_detail,
    CustomUserViewSet
)


router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)
router.register(
    prefix='user',
    viewset=CustomUserViewSet,
    basename='user',
)

urlpatterns = [
    path('api/', user_list, name='user-list'),
    path('api/<int:user_id>/', user_detail, name='user-detail'),
    path('v1/', include(router.urls))
]


