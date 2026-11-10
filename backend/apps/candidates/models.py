"""Candidate profile, education, experience, skills, saved jobs."""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.validators import resume_validator, validate_resume_size


class Candidate(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
    )
    headline = models.CharField(max_length=150, blank=True)
    summary = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=150, blank=True)
    resume = models.FileField(
        upload_to="resumes/", null=True, blank=True,
        validators=[resume_validator, validate_resume_size],
    )
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    years_of_experience = models.PositiveSmallIntegerField(default=0)
    is_open_to_work = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("candidate")
        verbose_name_plural = _("candidates")

    def __str__(self):
        return self.user.get_full_name() or self.user.email


class Education(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="education",
    )
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=150, blank=True)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("-end_year", "-start_year")

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="experience",
    )
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=150, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("-start_date",)

    def __str__(self):
        return f"{self.title} @ {self.company}"


class Skill(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="skills",
    )
    name = models.CharField(max_length=80)
    level = models.CharField(
        max_length=20, blank=True,
        choices=[("beginner", "Beginner"), ("intermediate", "Intermediate"),
                 ("advanced", "Advanced"), ("expert", "Expert")],
    )

    class Meta:
        unique_together = ("candidate", "name")
        ordering = ("name",)

    def __str__(self):
        return self.name


class SavedJob(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="saved_jobs",
    )
    job = models.ForeignKey(
        "jobs.Job", on_delete=models.CASCADE, related_name="saved_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("candidate", "job")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.candidate} saved {self.job}"