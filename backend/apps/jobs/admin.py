"""Admin for jobs."""
from django.contrib import admin
from django.utils.html import format_html

from .models import Job, JobCategory


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title", "company", "employer", "job_type", "location",
        "status", "is_featured", "applications_count", "created_at",
    )
    list_filter = ("status", "job_type", "is_remote", "is_featured", "category")
    search_fields = ("title", "company__name", "employer__email", "location")
    readonly_fields = ("views_count", "applications_count", "slug")
    date_hierarchy = "created_at"
    raw_id_fields = ("employer", "company")