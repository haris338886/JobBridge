"""Business logic for reviews."""
from __future__ import annotations

from django.db.models import Avg

from .models import Review


def company_average_rating(company) -> float:
    result = Review.objects.filter(company=company).aggregate(avg=Avg("rating"))
    return round(result["avg"] or 0, 2)