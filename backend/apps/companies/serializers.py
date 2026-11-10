"""DRF serializers for companies."""
from __future__ import annotations

from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    jobs_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = (
            "id", "name", "slug", "description", "website",
            "industry", "size", "location", "logo", "logo_url",
            "jobs_count", "created_at",
        )
        read_only_fields = ("id", "slug", "created_at", "logo_url", "jobs_count")

    def get_logo_url(self, obj):
        if not obj.logo:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url

    def get_jobs_count(self, obj):
        return obj.jobs.filter(status="active").count()

    def create(self, validated_data):
        user = self.context["request"].user
        return Company.objects.create(owner=user, **validated_data)