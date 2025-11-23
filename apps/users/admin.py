from django.contrib.admin import register
from unfold.admin import ModelAdmin
from .models import CustomUser, Profile, Media

# register User Admin App
@register(CustomUser)
class UserAdmin(ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('email', 'username')
    ordering = ('-created_at',)

#register Profile App
@register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('id', 'user', 'display_name', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('user__email', 'user__username', 'display_name')


#register Media App
@register(Media)
class MediaAdmin(ModelAdmin):
    ...