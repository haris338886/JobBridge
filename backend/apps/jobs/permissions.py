"""Permissions for jobs app."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsEmployerOrReadOnly(BasePermission):
    """Only employers can create; owners can edit/delete."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user and request.user.is_authenticated and request.user.is_employer
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.employer == request.user or request.user.is_staff


class IsJobOwner(BasePermission):
    message = "You do not own this job."

    def has_object_permission(self, request, view, obj):
        return obj.employer == request.user or request.user.is_staff