# Python modules
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Django modules    
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

# Project modules
from apps.users.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('apps.core.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('notification/', include('apps.notifications.urls')),
    # User's urls
    path('users/', include('apps.users.urls')),
    # Posts' urls
    path('posts/', include('apps.posts.urls')),
    path('events/', include('apps.events.urls')),
    path('communities/', include('apps.communities.urls')),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
