"""Serializers for applications."""
from __future__ import annotations

from rest_framework import serializers

from .models import Application


class ApplicationListSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(
        source="candidate.user.get_full_name", read_only=True,
    )
    candidate_email = serializers.CharField(
        source="candidate.user.email", read_only=True,
    )
    job_title = serializers.CharField(source="job.title", read_only=True)
    company_name = serializers.CharField(source="job.company.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Application
        fields = (
            "id", "job", "job_title", "company_name",
            "candidate", "candidate_name", "candidate_email",
            "status", "status_display",
            "created_at", "updated_at",
        )


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("job", "cover_letter", "resume")

    def validate_job(self, job):
        candidate = getattr(self.context["request"].user, "candidate_profile", None)
        if not candidate:
            raise serializers.ValidationError("You must be a candidate to apply.")
        if Application.objects.filter(job=job, candidate=candidate).exists():
            raise serializers.ValidationError("You have already applied to this job.")
        if not job.is_active:
            raise serializers.ValidationError(
                "This job is no longer accepting applications."
            )
        return job


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("status", "employer_notes", "rating")