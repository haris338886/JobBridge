"""API views for interviews."""
from rest_framework import permissions, viewsets

from .models import Interview
from .permissions import IsInterviewParticipant
from .serializers import InterviewSerializer
from .services import schedule_interview


class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsInterviewParticipant]

    def get_queryset(self):
        user = self.request.user
        qs = Interview.objects.select_related(
            "application__job__company", "application__candidate__user",
        )
        if user.is_employer:
            return qs.filter(application__job__employer=user)
        if user.is_candidate:
            return qs.filter(application__candidate__user=user)
        return qs.none()

    def perform_create(self, serializer):
        application = serializer.validated_data["application"]
        scheduled_at = serializer.validated_data["scheduled_at"]
        extra = {
            k: v for k, v in serializer.validated_data.items()
            if k not in ("application", "scheduled_at")
        }
        schedule_interview(application=application, scheduled_at=scheduled_at, **extra)