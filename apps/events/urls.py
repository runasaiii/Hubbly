from django.urls import path
from .views import (
    EventListView, EventDetailView,
    EventPageListView, EventPageDetailView,
)


urlpatterns = [
    # HTML pages (default)
    path('', EventPageListView.as_view(), name='event-page-list'),
    path('<uuid:pk>/', EventPageDetailView.as_view(), name='event-page-detail'),
    # Back-compat aliases
    path('page/', EventPageListView.as_view(), name='event-page-list-legacy'),
    path('page/<uuid:pk>/', EventPageDetailView.as_view(), name='event-page-detail-legacy'),

    # REST API
    path('api/', EventListView.as_view(), name='event-list'),
    path('api/<uuid:pk>/', EventDetailView.as_view(), name='event-detail'),
]


