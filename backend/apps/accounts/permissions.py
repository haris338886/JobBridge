"""Role-based DRF permissions."""
from rest_framework.permissions import BasePermission


class IsCandidate(BasePermission):
    message = "Only candidates can access this resource."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_candidate)


class IsEmployer(BasePermission):
    message = "Only employers can access this resource."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_employer)


class IsAdminRole(BasePermission):
    message = "Only administrators can access this resource."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_admin_role or request.user.is_staff)
        )


class IsOwnerOrAdmin(BasePermission):
    """Object-level check: owner or admin can access."""

    owner_field = "user"

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_admin_role:
            return True
        owner = getattr(obj, self.owner_field, None)
        return owner == request.user