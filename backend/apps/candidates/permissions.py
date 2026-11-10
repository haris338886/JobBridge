"""Permissions for candidates."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCandidateOwner(BasePermission):
    message = "You do not own this candidate profile."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_staff


class IsCandidate(BasePermission):
    message = "Only candidates can access this resource."

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated
            and request.user.is_candidate
        )