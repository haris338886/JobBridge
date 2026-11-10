"""Business logic for jobs."""
from __future__ import annotations

from django.db.models import F, Q
from django.utils import timezone

from .models import Job


def list_active_jobs(*, search: str = "", location: str = "", category_id: int | None = None):
    qs = Job.objects.filter(status="active")
    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if location:
        qs = qs.filter(location__icontains=location)
    if category_id:
        qs = qs.filter(category_id=category_id)
    qs = qs.filter(Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now()))
    return qs.select_related("company", "category").order_by("-created_at")


def featured_jobs(limit: int = 6):
    return (
        Job.objects.filter(status="active", is_featured=True)
        .select_related("company")
        .order_by("-created_at")[:limit]
    )


def increment_views(job: Job) -> None:
    Job.objects.filter(pk=job.pk).update(views_count=F("views_count") + 1)


def increment_applications(job: Job) -> None:
    Job.objects.filter(pk=job.pk).update(applications_count=F("applications_count") + 1)