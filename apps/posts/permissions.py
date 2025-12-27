from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Post


class IsPostAuthor(BasePermission):
    """
    Allows editing and deletion
    only by the post's author
    """

    def has_object_permission(self, request, view, obj: Post) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user
