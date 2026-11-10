"""JWT helpers built on djangorestframework-simplejwt."""
from __future__ import annotations

from typing import Any

from rest_framework_simplejwt.tokens import RefreshToken


def tokens_for_user(user) -> dict[str, Any]:
    """
    Return ``{"access": "...", "refresh": "..."}`` for the given user.
    Adds a few custom claims for the frontend.
    """
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user.role
    refresh["email"] = user.email
    refresh["full_name"] = user.get_full_name()
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }