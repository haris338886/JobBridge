"""Business logic for applications."""
from __future__ import annotations

from django.db import transaction

from apps.notifications.services import create_notification

from .models import Application


@transaction.atomic
def create_application(*, job, candidate, **data) -> Application:
    application = Application.objects.create(job=job, candidate=candidate, **data)

    from apps.jobs.services import increment_applications
    increment_applications(job)

    create_notification(
        user=job.employer,
        title="New application received",
        message=f"{candidate} applied for {job.title}.",
        notif_type="application",
        link=f"/employer/applicants/{application.pk}/",
    )
    create_notification(
        user=candidate.user,
        title="Application received",
        message=f"Your application for {job.title} was received.",
        notif_type="application",
        link=f"/candidate/applications/{application.pk}/",
    )
    return application


@transaction.atomic
def update_status(application: Application, new_status: str, notes: str = "") -> Application:
    application.status = new_status
    if notes:
        application.employer_notes = notes
    application.save(update_fields=["status", "employer_notes", "updated_at"])
    create_notification(
        user=application.candidate.user,
        title=f"Application {new_status}",
        message=f"Your application for {application.job.title} is now {new_status}.",
        notif_type="application",
    )
    return application