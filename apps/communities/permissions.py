from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Community


class IsCommunityOwner(BasePermission):
    """
    Разрешает изменение и удаление
    только владельцу сообщества
    """

    def has_object_permission(self, request, view, obj: Community) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user
