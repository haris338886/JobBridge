"""Admin for interviews."""
from django.contrib import admin

from .models import Interview


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ("application", "scheduled_at", "interview_type", "status")
    list_filter = ("status", "interview_type")
    search_fields = ("application__job__title", "application__candidate__user__email")
    raw_id_fields = ("application",)