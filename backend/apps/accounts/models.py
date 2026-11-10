"""User and Profile models for JobBridge."""
from __future__ import annotations

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.

    - Email is the unique identifier (case-insensitive).
    - ``username`` is optional and used for display only.
    - ``role`` decides which dashboard the user sees.
    """

    class Role(models.TextChoices):
        CANDIDATE = "candidate", _("Candidate")
        EMPLOYER = "employer", _("Employer")
        ADMIN = "admin", _("Administrator")

    email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )
    first_name = models.CharField(_("first name"), max_length=60, blank=True)
    last_name = models.CharField(_("last name"), max_length=60, blank=True)

    role = models.CharField(
        _("role"),
        max_length=20,
        choices=Role.choices,
        default=Role.CANDIDATE,
        db_index=True,
    )

    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_verified = models.BooleanField(_("email verified"), default=False)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    # Managers -----------------------------------------------------
    objects = UserManager()

    # Django auth wiring -------------------------------------------
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # superuser creation prompts only for email + password

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-date_joined",)

    # Dunder -------------------------------------------------------
    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_short_name(self) -> str:
        return self.first_name or self.email.split("@")[0]

    # Role helpers ------------------------------------------------
    @property
    def is_candidate(self) -> bool:
        return self.role == self.Role.CANDIDATE

    @property
    def is_employer(self) -> bool:
        return self.role == self.Role.EMPLOYER

    @property
    def is_admin_role(self) -> bool:
        return self.role == self.Role.ADMIN


class Profile(models.Model):
    """
    Extra per-user data that doesn't fit on the auth table
    (avatar, bio, phone, location).
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(
        upload_to="profile-images/",
        null=True,
        blank=True,
    )
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self) -> str:
        return f"Profile of {self.user.email}"