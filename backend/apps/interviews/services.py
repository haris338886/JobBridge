"""Business logic for interviews."""
from __future__ import annotations

from django.db import transaction

from apps.notifications.services import create_notification

from .models import Interview


@transaction.atomic
def schedule_interview(*, application, scheduled_at, **data) -> Interview:
    interview = Interview.objects.create(
        application=application,
        scheduled_at=scheduled_at,
        **data,
    )
    # Move the application into the "interview" state.
    if application.status != "interview":
        application.status = "interview"
        application.save(update_fields=["status"])

    create_notification(
        user=application.candidate.user,
        title="Interview scheduled",
        message=(
            f"You have an interview for {application.job.title} on "
            f"{scheduled_at:%B %d, %Y at %H:%M}."
        ),
        notif_type="interview",
        link=f"/candidate/interviews/{interview.pk}/",
    )
    return interview