"""Generic helpers."""
from __future__ import annotations

import secrets
import string
from datetime import date
from typing import Any

from django.utils.text import slugify


def unique_slug(instance, base: str, field: str = "slug", max_length: int = 100) -> str:
    """
    Generate a unique slug for ``instance`` based on ``base``.
    Appends ``-1``, ``-2``, etc. if collision.
    """
    ModelClass = instance.__class__
    base_slug = slugify(base)[:max_length] or "item"
    slug = base_slug
    counter = 1
    while ModelClass.objects.filter(**{field: slug}).exists():
        suffix = f"-{counter}"
        slug = f"{base_slug[: max_length - len(suffix)]}{suffix}"
        counter += 1
    return slug


def generate_token(length: int = 32) -> str:
    """Cryptographically strong random token (URL-safe)."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def human_date(d: date | None) -> str:
    if not d:
        return ""
    return d.strftime("%B %d, %Y")


def mask_email(email: str) -> str:
    try:
        local, domain = email.split("@", 1)
    except ValueError:
        return email
    if len(local) <= 2:
        local_masked = local[0] + "*"
    else:
        local_masked = local[0] + "*" * (len(local) - 2) + local[-1]
    return f"{local_masked}@{domain}"


def dict_subset(d: dict, keys: list[str]) -> dict[str, Any]:
    return {k: d[k] for k in keys if k in d}