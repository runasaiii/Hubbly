#Django modules
from django.shortcuts import render
from django.views.generic import ListView, DetailView

#DRF
from rest_framework import generics

#App modules
from .models import Community
from .serializers import CommunitySerializer


class CommunityListView(generics.ListCreateAPIView):
    """
    Community List View controller
    """
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Community Detail View controller
    """
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CommunityPageListView(ListView):
    """
    Community Page List View controller
    """
    model = Community
    template_name = 'communities/community_list.html'
    context_object_name = 'communities'


class CommunityPageDetailView(DetailView):
    """
    Community Page Detail View controller
    """
    model = Community
    template_name = 'communities/community_detail.html'
    context_object_name = 'community'
