"""Serializers for reviews."""
from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Review
        fields = (
            "id", "company", "company_name",
            "candidate", "candidate_name",
            "rating", "title", "body", "is_anonymous",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at", "candidate")

    def get_candidate_name(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return obj.candidate.user.get_full_name()

    def create(self, validated_data):
        candidate = self.context["request"].user.candidate_profile
        return Review.objects.create(candidate=candidate, **validated_data)