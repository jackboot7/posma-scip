from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj=None):
        # Write permissions are only allowed to the owner of the snippet
        return obj is None or obj == request.user or request.user.is_staff
