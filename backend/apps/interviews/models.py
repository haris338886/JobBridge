"""Interview model."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.constants import InterviewStatus, InterviewType


class Interview(models.Model):
    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="interviews",
    )
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveSmallIntegerField(default=60)
    interview_type = models.CharField(
        max_length=20, choices=InterviewType.CHOICES,
        default=InterviewType.VIDEO,
    )
    location = models.CharField(max_length=255, blank=True)
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=InterviewStatus.CHOICES,
        default=InterviewStatus.SCHEDULED, db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("interview")
        verbose_name_plural = _("interviews")
        ordering = ("-scheduled_at",)

    def __str__(self):
        return f"{self.application} @ {self.scheduled_at:%Y-%m-%d %H:%M}"