"""Config for applications app."""
from django.apps import AppConfig


class ApplicationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.applications"
    label = "applications"
    verbose_name = "Applications"

    def ready(self):
        from . import signals  # noqa: F401