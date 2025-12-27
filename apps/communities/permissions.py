from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Community


class IsCommunityOwner(BasePermission):
    """
    Allows editing and deletion
    Only by the community owner
    """

    def has_object_permission(self, request, view, obj: Community) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user
