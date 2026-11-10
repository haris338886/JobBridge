"""Application model."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.constants import ApplicationStatus


class Application(models.Model):
    job = models.ForeignKey(
        "jobs.Job", on_delete=models.CASCADE, related_name="applications",
    )
    candidate = models.ForeignKey(
        "candidates.Candidate", on_delete=models.CASCADE, related_name="applications",
    )
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)

    status = models.CharField(
        max_length=20, choices=ApplicationStatus.CHOICES,
        default=ApplicationStatus.APPLIED, db_index=True,
    )
    employer_notes = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("application")
        verbose_name_plural = _("applications")
        ordering = ("-created_at",)
        unique_together = ("job", "candidate")

    def __str__(self):
        return f"{self.candidate} → {self.job}"

    @property
    def status_display(self):
        return self.get_status_display()