from django.shortcuts import render
from rest_framework import generics
from django.views.generic import ListView, DetailView
from .models import Community
from .serializers import CommunitySerializer


class CommunityListView(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class CommunityPageListView(ListView):
    model = Community
    template_name = 'communities/community_list.html'
    context_object_name = 'communities'


class CommunityPageDetailView(DetailView):
    model = Community
    template_name = 'communities/community_detail.html'
    context_object_name = 'community'
