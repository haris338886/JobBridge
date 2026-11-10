"""Admin for reviews."""
from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("company", "candidate", "rating", "is_anonymous", "created_at")
    list_filter = ("rating", "is_anonymous")
    search_fields = ("company__name", "candidate__user__email", "title")
    raw_id_fields = ("company", "candidate")