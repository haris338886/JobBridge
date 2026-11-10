"""Business logic for notifications."""
from __future__ import annotations

from .models import Notification


def create_notification(*, user, title: str, message: str,
                        notif_type: str = "system",
                        link: str = "") -> Notification:
    return Notification.objects.create(
        user=user, title=title, message=message,
        notif_type=notif_type, link=link,
    )


def mark_all_read(user) -> int:
    return Notification.objects.filter(user=user, is_read=False).update(is_read=True)