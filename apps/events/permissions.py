from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from .models import Event


class IsEventOrganizer(BasePermission):
    """
    Allows editing and deletion
    Only by the event organizer
    """

    def has_object_permission(self, request: Request, view, obj: Event) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.organizer == request.user
