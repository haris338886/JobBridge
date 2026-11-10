"""Custom user manager (email-based login)."""
from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Manager for the custom ``User`` model.

    ``email`` is the unique identifier — ``username`` is optional and
    only used for display.
    """

    use_in_migrations = True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _create_user(
        self,
        email: str,
        password: str | None,
        **extra_fields: Any,
    ):
        if not email:
            raise ValueError(_("The email address must be set."))

        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def create_user(self, email: str, password: str | None = None, **extra_fields: Any):
        extra_fields.setdefault("role", self.model.Role.CANDIDATE)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: Any):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", self.model.Role.ADMIN)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)

    # ------------------------------------------------------------------
    # Lookup helpers
    # ------------------------------------------------------------------
    def get_by_natural_key(self, username: str):
        """Allow Django auth to look up by email (the natural key)."""
        return self.get(email__iexact=username)