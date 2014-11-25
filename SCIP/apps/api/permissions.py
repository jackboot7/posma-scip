from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow the corresponding user to handle data related to himself.
    """

    def has_object_permission(self, request, view, obj=None):
        # obj must be an instance of django.contrib.auth.models.User
        return obj is None or obj == request.user or request.user.is_staff
