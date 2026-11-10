"""Shared DRF permission classes."""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Anyone can read; only the owner can write."""
    owner_field = "owner"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = getattr(obj, self.owner_field, None)
        return owner == request.user


class IsSameUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsEmployerOwner(BasePermission):
    """Only the employer who owns the job/company can modify."""
    message = "You do not own this resource."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_admin_role:
            return True
        owner = getattr(obj, "employer", None) or getattr(obj, "company", None)
        if owner is None and hasattr(obj, "company"):
            owner = obj.company.owner
        return owner == user