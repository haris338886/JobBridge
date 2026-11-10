"""Permissions for applications."""
from rest_framework.permissions import BasePermission


class IsApplicationCandidate(BasePermission):
    message = "Only the applicant can access this application."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.candidate.user == request.user


class IsApplicationEmployer(BasePermission):
    message = "Only the employer for this job can access this application."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.job.employer == request.user