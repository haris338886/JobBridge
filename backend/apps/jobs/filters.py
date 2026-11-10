"""django-filter filterset for jobs."""
from django_filters import rest_framework as filters

from .models import Job


class JobFilter(filters.FilterSet):
    q = filters.CharFilter(method="filter_search")
    location = filters.CharFilter(field_name="location", lookup_expr="icontains")
    category = filters.NumberFilter(field_name="category_id")
    job_type = filters.CharFilter(field_name="job_type")
    is_remote = filters.BooleanFilter(field_name="is_remote")
    salary_min = filters.NumberFilter(field_name="salary_min", lookup_expr="gte")
    salary_max = filters.NumberFilter(field_name="salary_max", lookup_expr="lte")
    status = filters.CharFilter(field_name="status")
    featured = filters.BooleanFilter(field_name="is_featured")

    class Meta:
        model = Job
        fields = [
            "q", "location", "category", "job_type",
            "is_remote", "salary_min", "salary_max",
            "status", "featured",
        ]

    def filter_search(self, qs, name, value):
        return qs.filter(title__icontains=value) | qs.filter(description__icontains=value)