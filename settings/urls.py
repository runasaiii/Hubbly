# Django Rest Framework Modules
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.permissions import AllowAny

# Swagger Modules
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


# Django modules    
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# Project modules
from apps.users.views import CustomTokenObtainPairView

# Django Toolbar
from debug_toolbar.toolbar import debug_toolbar_urls


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
    # Swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + debug_toolbar_urls()

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
