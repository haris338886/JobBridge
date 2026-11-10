"""Job and JobCategory models."""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.constants import JobStatus, JobType
from common.utils import unique_slug


class JobCategory(models.Model):
    name = models.CharField(_("name"), max_length=80, unique=True)
    slug = models.SlugField(_("slug"), max_length=90, unique=True, blank=True)
    description = models.TextField(_("description"), blank=True)
    icon = models.CharField(_("icon"), max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("job category")
        verbose_name_plural = _("job categories")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name, "slug", max_length=90)
        super().save(*args, **kwargs)


class Job(models.Model):
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posted_jobs",
        limit_choices_to={"role": "employer"},
    )
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    category = models.ForeignKey(
        JobCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="jobs",
    )
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=220, unique=True, blank=True)
    description = models.TextField(_("description"))
    requirements = models.TextField(_("requirements"), blank=True)
    responsibilities = models.TextField(_("responsibilities"), blank=True)

    job_type = models.CharField(
        _("job type"), max_length=20,
        choices=JobType.CHOICES, default=JobType.FULL_TIME,
    )
    location = models.CharField(_("location"), max_length=150)
    is_remote = models.BooleanField(_("remote allowed"), default=False)

    salary_min = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
    )
    salary_max = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
    )
    salary_currency = models.CharField(max_length=3, default="USD")

    experience_years = models.PositiveSmallIntegerField(
        _("years of experience"), null=True, blank=True,
    )
    vacancies = models.PositiveSmallIntegerField(default=1)

    status = models.CharField(
        max_length=20, choices=JobStatus.CHOICES,
        default=JobStatus.ACTIVE, db_index=True,
    )
    expires_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    views_count = models.PositiveIntegerField(default=0)
    applications_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("job")
        verbose_name_plural = _("jobs")
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["location"]),
            models.Index(fields=["job_type"]),
        ]

    def __str__(self):
        return f"{self.title} @ {self.company}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.title} {self.company.name if self.company_id else ''}"
            self.slug = unique_slug(self, base, "slug", max_length=220)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # FIX: url uses <slug:slug>, not <pk>
        return reverse("marketing:job_detail", kwargs={"slug": self.slug})

    @property
    def salary_range(self) -> str:
        if self.salary_min and self.salary_max:
            return f"{self.salary_currency} {self.salary_min:,.0f} – {self.salary_max:,.0f}"
        if self.salary_min:
            return f"{self.salary_currency} {self.salary_min:,.0f}+"
        return ""

    @property
    def is_active(self) -> bool:
        if self.status != JobStatus.ACTIVE:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True