"""Permissions for interviews."""
from rest_framework.permissions import BasePermission


class IsInterviewParticipant(BasePermission):
    message = "You are not a participant in this interview."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True
        return (
            obj.application.job.employer == user
            or obj.application.candidate.user == user
        )