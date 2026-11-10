"""Permissions for reviews."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsReviewOwner(BasePermission):
    message = "You did not write this review."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.candidate.user == request.user or request.user.is_staff