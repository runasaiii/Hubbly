from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView
from .models import User
from .serializers import UserSerializer


def user_list(request):
    """
    User List controller
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)

def user_detail(request, user_id):
    """
    User Detail controller
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)

class UserPageListView(ListView):
    """
    User Page List View controller
    """
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserPageDetailView(DetailView):
    """
    User Page Detail View controller
    """
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user_obj'
