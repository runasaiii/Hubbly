from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User, Profile


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('email', 'username')
    ordering = ('-created_at',)


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('id', 'user', 'display_name', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('user__email', 'user__username', 'display_name')
    