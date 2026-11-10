"""Business logic for accounts (register, verify, reset)."""
from __future__ import annotations

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import Profile

User = get_user_model()
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Registration
# ----------------------------------------------------------------------
@transaction.atomic
def register_user(
    *, email: str, password: str, role: str, **extra
) -> AbstractBaseUser:
    user = User.objects.create_user(
        email=email, password=password, role=role, **extra,
    )
    Profile.objects.get_or_create(user=user)
    send_verification_email(user)
    return user


# ----------------------------------------------------------------------
# Email verification
# ----------------------------------------------------------------------
def build_verification_url(user: AbstractBaseUser) -> str:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    path = reverse(
        "accounts:verify_email_confirm",
        kwargs={"uidb64": uid, "token": token},
    )
    return f"{settings.FRONTEND_URL}{path}"


def send_verification_email(user: AbstractBaseUser) -> None:
    url = build_verification_url(user)
    subject = "Verify your JobBridge email"
    message = (
        f"Hi {user.get_full_name() or user.email},\n\n"
        f"Please verify your email by clicking this link:\n{url}\n\n"
        "If you didn't sign up, ignore this email."
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )


def verify_email_token(uidb64: str, token: str) -> AbstractBaseUser | None:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        return None
    if not default_token_generator.check_token(user, token):
        return None
    if not user.is_verified:
        user.is_verified = True
        user.save(update_fields=["is_verified"])
    return user


# ----------------------------------------------------------------------
# Password reset
# ----------------------------------------------------------------------
def send_password_reset_email(email: str) -> None:
    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        logger.info("Password reset requested for unknown email %s", email)
        return

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    url = (
        f"{settings.FRONTEND_URL}"
        f"{reverse('accounts:reset_password_confirm', kwargs={'uidb64': uid, 'token': token})}"
    )
    subject = "Reset your JobBridge password"
    message = (
        f"Hi {user.get_full_name() or user.email},\n\n"
        f"Click this link to reset your password:\n{url}\n\n"
        "If you didn't request it, you can ignore this email."
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )


def reset_password_with_token(
    uidb64: str, token: str, new_password: str,
) -> AbstractBaseUser | None:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        return None
    if not default_token_generator.check_token(user, token):
        return None
    user.set_password(new_password)
    user.save(update_fields=["password"])
    return user