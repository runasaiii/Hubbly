# Django modules
from django.urls import path, include

# Project modules
from .views import (
    user_list,
    user_detail,
    UserPageListView,
    UserPageDetailView,
    CustomUserViewSet
)
# Django Rest Framework modules
from rest_framework.routers import DefaultRouter

router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)
router.register(
    prefix='user',
    viewset=CustomUserViewSet,
    basename='user',
)
urlpatterns = [
    # HTML pages (default)
    path('', UserPageListView.as_view(), name='user-page-list'),
    path('<int:pk>/', UserPageDetailView.as_view(), name='user-page-detail'),
    # Back-compat aliases
    path('page/', UserPageListView.as_view(), name='user-page-list-legacy'),
    path('page/<int:pk>/', UserPageDetailView.as_view(), name='user-page-detail-legacy'),

    # REST API
    path('api/', user_list, name='user-list'),
    path('api/<int:user_id>/', user_detail, name='user-detail'),
    path('v1/', include(router.urls))
]


