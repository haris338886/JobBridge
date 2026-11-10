"""Business logic for candidates."""
from __future__ import annotations

from .models import Candidate


def get_or_create_candidate(user) -> Candidate:
    candidate, _ = Candidate.objects.get_or_create(user=user)
    return candidate