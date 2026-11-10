"""Serializers for interviews."""
from __future__ import annotations

from rest_framework import serializers

from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(
        source="application.candidate.user.get_full_name", read_only=True,
    )
    job_title = serializers.CharField(source="application.job.title", read_only=True)
    interview_type_display = serializers.CharField(
        source="get_interview_type_display", read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True,
    )

    class Meta:
        model = Interview
        fields = (
            "id", "application", "candidate_name", "job_title",
            "scheduled_at", "duration_minutes",
            "interview_type", "interview_type_display",
            "location", "meeting_link", "notes",
            "status", "status_display",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")