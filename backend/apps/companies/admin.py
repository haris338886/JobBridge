"""Admin for companies."""
from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "industry", "size", "location", "created_at")
    list_filter = ("industry", "size")
    search_fields = ("name", "owner__email", "location")
    prepopulated_fields = {"slug": ("name",)}
    raw_id_fields = ("owner",)