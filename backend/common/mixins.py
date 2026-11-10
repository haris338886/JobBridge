"""Reusable DRF view mixins."""
from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class RoleRequiredMixin(LoginRequiredMixin):
    """
    Require the logged-in user to have one of the given roles.

    Usage:
        class Dashboard(RoleRequiredMixin, TemplateView):
            required_roles = ("candidate",)
    """
    required_roles: tuple[str, ...] = ()
    redirect_url: str | None = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.required_roles and request.user.role not in self.required_roles:
            if self.redirect_url:
                return redirect(self.redirect_url)
            raise PermissionDenied("You do not have access to this page.")
        return super().dispatch(request, *args, **kwargs)


class OwnerQuerysetMixin:
    """Restrict a ListView queryset to the current user."""
    owner_field = "user"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff or getattr(user, "is_admin_role", False):
            return qs
        return qs.filter(**{self.owner_field: user})