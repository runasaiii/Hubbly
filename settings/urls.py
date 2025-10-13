from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('apps.core.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('apps.users.urls')),
    path('posts/', include('apps.posts.urls')),
    path('events/', include('apps.events.urls')),
    path('communities/', include('apps.communities.urls')),
]
