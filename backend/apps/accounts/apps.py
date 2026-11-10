"""Config for the accounts app."""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
    verbose_name = "Accounts & Authentication"

    def ready(self) -> None:
        # Import signal handlers so they register on app load.
        from . import signals  # noqa: F401