"""Serializers for candidates."""
from __future__ import annotations

from rest_framework import serializers

from .models import Candidate, Education, Experience, SavedJob, Skill


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"
        read_only_fields = ("candidate",)


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = ("candidate",)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("id", "name", "level")
        read_only_fields = ("id",)


class CandidateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = (
            "id", "email", "full_name", "headline", "summary",
            "phone", "location", "resume", "linkedin", "portfolio",
            "years_of_experience", "is_open_to_work",
            "education", "experience", "skills",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "email", "full_name", "created_at", "updated_at")


class SavedJobSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    company_name = serializers.CharField(source="job.company.name", read_only=True)

    class Meta:
        model = SavedJob
        fields = ("id", "job", "job_title", "company_name", "created_at")
        read_only_fields = ("id", "created_at", "job_title", "company_name")