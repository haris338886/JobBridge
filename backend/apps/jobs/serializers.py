"""DRF serializers for jobs."""
from __future__ import annotations

from rest_framework import serializers

from .models import Job, JobCategory


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ("id", "name", "slug", "description", "icon")
        read_only_fields = ("id", "slug")


class JobListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_logo = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)
    salary_range = serializers.CharField(read_only=True)

    class Meta:
        model = Job
        fields = (
            "id", "title", "slug", "company_name", "company_logo",
            "category_name", "job_type", "location", "is_remote",
            "salary_range", "status", "created_at", "expires_at",
            "views_count", "applications_count", "is_featured",
        )

    def get_company_logo(self, obj):
        if not obj.company.logo:
            return None
        request = self.context.get("request")
        return (
            request.build_absolute_uri(obj.company.logo.url)
            if request else obj.company.logo.url
        )


class JobDetailSerializer(JobListSerializer):
    description = serializers.CharField()
    requirements = serializers.CharField()
    responsibilities = serializers.CharField()
    salary_min = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True, required=False,
    )
    salary_max = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True, required=False,
    )
    salary_currency = serializers.CharField(required=False)
    experience_years = serializers.IntegerField(
        allow_null=True, required=False,
    )
    vacancies = serializers.IntegerField(required=False)

    class Meta(JobListSerializer.Meta):
        fields = JobListSerializer.Meta.fields + (
            "description", "requirements", "responsibilities",
            "salary_min", "salary_max", "salary_currency",
            "experience_years", "vacancies",
        )


class JobCreateUpdateSerializer(serializers.ModelSerializer):
    # Accept empty string / null for category so the form works
    # even when no JobCategory rows have been seeded.
    category = serializers.PrimaryKeyRelatedField(
        queryset=JobCategory.objects.all(),
        required=False,
        allow_null=True,
    )

    # The HTML form sends `salary_range` as free text.
    # We split it into salary_min / salary_max on save.
    salary_range = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = Job
        fields = (
            "title", "description", "requirements", "responsibilities",
            "category", "job_type", "location", "is_remote",
            "salary_min", "salary_max", "salary_currency",
            "experience_years", "vacancies", "expires_at",
            "salary_range",  # virtual, write-only
        )

    def to_internal_value(self, data):
        # Convert empty-string category -> None before validation
        if hasattr(data, "copy"):
            data = data.copy()
        if "category" in data and data["category"] in ("", None):
            data["category"] = None
        return super().to_internal_value(data)

    def validate(self, attrs):
        smin = attrs.get("salary_min")
        smax = attrs.get("salary_max")
        if smin is not None and smax is not None and smin > smax:
            raise serializers.ValidationError(
                {"salary_max": "Max salary must be greater than min salary."}
            )

        # If salary_range provided (e.g. "$60k-$80k"), parse it best-effort
        range_text = attrs.pop("salary_range", "") or ""
        range_text = range_text.strip()
        if range_text and smin is None and smax is None:
            numbers = []
            for token in range_text.replace(",", " ").split():
                cleaned = "".join(c for c in token if c.isdigit() or c == ".")
                if cleaned:
                    try:
                        numbers.append(float(cleaned))
                    except ValueError:
                        pass
            if len(numbers) >= 2:
                attrs["salary_min"] = numbers[0]
                attrs["salary_max"] = numbers[1]
            elif len(numbers) == 1:
                attrs["salary_min"] = numbers[0]

        return attrs

    def create(self, validated_data):
        company = validated_data.pop("company", None)
        if company is None:
            user = self.context["request"].user
            company = user.companies.first()
            if not company:
                from apps.companies.models import Company
                company = Company.objects.create(
                    owner=user,
                    name=f"{user.get_full_name() or user.email}'s Company",
                )
        return Job.objects.create(
            employer=self.context["request"].user,
            company=company,
            **validated_data,
        )