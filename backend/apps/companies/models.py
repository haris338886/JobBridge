"""Company model."""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from common.utils import unique_slug


class Company(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="companies",
        limit_choices_to={"role": "employer"},
    )
    name = models.CharField(_("name"), max_length=150)
    slug = models.SlugField(_("slug"), max_length=170, unique=True, blank=True)
    description = models.TextField(_("description"), blank=True)
    website = models.URLField(_("website"), blank=True)
    industry = models.CharField(_("industry"), max_length=100, blank=True)
    size = models.CharField(
        _("size"), max_length=20, blank=True,
        choices=[
            ("1-10", "1-10"),
            ("11-50", "11-50"),
            ("51-200", "51-200"),
            ("201-500", "201-500"),
            ("500+", "500+"),
        ],
    )
    logo = models.ImageField(
        _("logo"), upload_to="company-logos/", null=True, blank=True,
    )
    location = models.CharField(_("location"), max_length=150, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("company")
        verbose_name_plural = _("companies")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name, "slug", max_length=170)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("marketing:job_list") + f"?company={self.slug}"