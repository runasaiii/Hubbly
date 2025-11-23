# Python modules
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

# Django modules
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView

# Project modules
from .models import CustomUser
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    RegistrationSerializer,
)


def user_list(request):
    """
    User List controller
    """
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)

def user_detail(request, user_id):
    """
    User Detail controller
    """
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=404)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)

class UserPageListView(ListView):
    """
    User Page List View controller
    """
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserPageDetailView(DetailView):
    """
    User Page Detail View controller
    """
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'user_obj'


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom Token Obtain Pair View using CustomTokenObtainPairSerializer
    """
    serializer_class = CustomTokenObtainPairSerializer

class RegistrationView(generics.CreateAPIView):
    """
    User Registration View
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer