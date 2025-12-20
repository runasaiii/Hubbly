# Django Modules
from django.urls import path

# Project Modules
from .views import (
    EventListView, EventDetailView,
    EventPageListView, EventPageDetailView,
)


urlpatterns = [
    path('', EventPageListView.as_view(), name='event-page-list'),
    path('<uuid:pk>/', EventPageDetailView.as_view(), name='event-page-detail'),

    path('page/', EventPageListView.as_view(), name='event-page-list-legacy'),
    path('page/<uuid:pk>/', EventPageDetailView.as_view(), name='event-page-detail-legacy'),

    # rest apishki
    path('api/', EventListView.as_view(), name='event-list'),
    path('api/<uuid:pk>/', EventDetailView.as_view(), name='event-detail'),
]


