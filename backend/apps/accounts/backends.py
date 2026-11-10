"""Authentication backend that accepts email or username."""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """Allow login with either ``email`` or ``username``."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username or kwargs.get("email") or kwargs.get("username")
        if identifier is None or password is None:
            return None

        try:
            user = User.objects.get(
                Q(email__iexact=identifier) | Q(username__iexact=identifier)
            )
        except User.DoesNotExist:
            # Run the default hasher to reduce timing attacks
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(
                Q(email__iexact=identifier) | Q(username__iexact=identifier)
            ).order_by("id").first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None