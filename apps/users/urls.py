from django.urls import path
from .views import user_list, user_detail, UserPageListView, UserPageDetailView


urlpatterns = [
    # HTML pages (default)
    path('', UserPageListView.as_view(), name='user-page-list'),
    path('<uuid:pk>/', UserPageDetailView.as_view(), name='user-page-detail'),
    # Back-compat aliases
    path('page/', UserPageListView.as_view(), name='user-page-list-legacy'),
    path('page/<uuid:pk>/', UserPageDetailView.as_view(), name='user-page-detail-legacy'),

    # REST API
    path('api/', user_list, name='user-list'),
    path('api/<uuid:user_id>/', user_detail, name='user-detail'),
]


