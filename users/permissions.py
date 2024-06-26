from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False


class IsOwner(BasePermission):
    """Доступно владельцам."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
