"""Business logic for companies."""
from __future__ import annotations

from .models import Company


def get_or_create_company_for_user(user) -> Company:
    company = user.companies.first()
    if company:
        return company
    return Company.objects.create(
        owner=user,
        name=f"{user.get_full_name() or user.email}'s Company",
    )