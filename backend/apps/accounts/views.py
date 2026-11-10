"""API + HTML views for accounts."""
from __future__ import annotations

from django.conf import settings
from django.contrib import messages as flash
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    RequestPasswordResetSerializer,
    ResetPasswordSerializer,
    UserSerializer,
)
from .services import (
    register_user,
    reset_password_with_token,
    send_password_reset_email,
    verify_email_token,
)
from .tokens import tokens_for_user

User = get_user_model()

# The backend string we must pass to login() when we create the user
# manually (bypassing authenticate()). Both backends can log in any
# user, so we just pick the primary one.
LOGIN_BACKEND = "apps.accounts.backends.EmailOrUsernameBackend"


# ======================================================================
# HTML views
# ======================================================================

class LoginView(TemplateView):
    template_name = "authentication/login.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        identifier = (
            request.POST.get("email")
            or request.POST.get("identifier")
            or ""
        ).strip()
        password = request.POST.get("password") or ""

        user = authenticate(request=request, username=identifier, password=password)
        if not user:
            flash.error(request, "Invalid credentials.")
            return render(request, self.template_name, {"identifier": identifier})

        # authenticate() already set user.backend, so plain login works here
        login(request, user)

        if user.is_candidate:
            return redirect("candidates:dashboard")
        if user.is_employer:
            return redirect("employers:dashboard")
        return redirect("marketing:index")


class RegisterChoiceView(TemplateView):
    """Choose between candidate or employer registration."""
    template_name = "authentication/register-choice.html"


class RegisterCandidateView(TemplateView):
    template_name = "authentication/register-candidate.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if password != password2:
            flash.error(request, "Passwords do not match.")
            return render(request, self.template_name, request.POST)

        try:
            user = register_user(
                email=email,
                password=password,
                role=User.Role.CANDIDATE,
                first_name=request.POST.get("first_name", "").strip(),
                last_name=request.POST.get("last_name", "").strip(),
            )
        except Exception as exc:  # noqa: BLE001
            flash.error(request, str(exc))
            return render(request, self.template_name, request.POST)

        # ⬇⬇⬇ THE FIX ⬇⬇⬇
        login(request, user, backend=LOGIN_BACKEND)

        flash.success(request, "Welcome! Check your email to verify your account.")
        return redirect("candidates:dashboard")


class RegisterEmployerView(TemplateView):
    template_name = "authentication/register-employer.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if password != password2:
            flash.error(request, "Passwords do not match.")
            return render(request, self.template_name, request.POST)

        try:
            user = register_user(
                email=email,
                password=password,
                role=User.Role.EMPLOYER,
                first_name=request.POST.get("first_name", "").strip(),
                last_name=request.POST.get("last_name", "").strip(),
            )
        except Exception as exc:  # noqa: BLE001
            flash.error(request, str(exc))
            return render(request, self.template_name, request.POST)

        try:
            from apps.companies.models import Company
            company_name = request.POST.get("company_name", "").strip()
            if company_name:
                Company.objects.create(owner=user, name=company_name)
        except Exception:  # noqa: BLE001
            pass

        # ⬇⬇⬇ THE FIX ⬇⬇⬇
        login(request, user, backend=LOGIN_BACKEND)

        flash.success(request, "Account created! Check your email to verify.")
        return redirect("employers:dashboard")


class ForgotPasswordView(TemplateView):
    template_name = "authentication/forgot-password.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.POST.get("email", "").strip()
        send_password_reset_email(email)
        flash.success(request, "If that email exists, a reset link was sent.")
        return redirect("accounts:login")


class ResetPasswordView(TemplateView):
    template_name = "authentication/reset-password.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["uidb64"] = self.kwargs.get("uidb64", "")
        ctx["token"] = self.kwargs.get("token", "")
        return ctx

    def post(self, request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
        password = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if password != password2:
            flash.error(request, "Passwords do not match.")
            return render(request, self.template_name)

        user = reset_password_with_token(uidb64, token, password)
        if not user:
            flash.error(request, "Invalid or expired token.")
            return redirect("accounts:forgot_password")

        flash.success(request, "Password updated. Please log in.")
        return redirect("accounts:login")


class VerifyEmailView(TemplateView):
    template_name = "authentication/verify-email.html"

    def get(self, request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
        user = verify_email_token(uidb64, token)
        ctx = {"success": bool(user)}
        if user:
            flash.success(request, "Email verified — you're all set!")
        else:
            flash.error(request, "Verification link is invalid or expired.")
        return render(request, self.template_name, ctx)


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = "authentication/change-password.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        old = request.POST.get("old_password", "")
        new1 = request.POST.get("new_password1", "")
        new2 = request.POST.get("new_password2", "")

        if not request.user.check_password(old):
            flash.error(request, "Current password is incorrect.")
        elif new1 != new2:
            flash.error(request, "Passwords do not match.")
        elif not new1:
            flash.error(request, "New password cannot be empty.")
        else:
            request.user.set_password(new1)
            request.user.save(update_fields=["password"])
            flash.success(request, "Password updated.")
            return redirect("accounts:login")

        return render(request, self.template_name)


@require_http_methods(["GET", "POST"])
def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    flash.success(request, "You have been logged out.")
    return redirect("accounts:login")


# ======================================================================
# API views
# ======================================================================

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "tokens": tokens_for_user(user),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(
            {
                "user": UserSerializer(user, context={"request": request}).data,
                "tokens": tokens_for_user(user),
            }
        )


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
            token = request.data.get("refresh")
            if token:
                RefreshToken(token).blacklist()
        except Exception:  # noqa: BLE001
            pass
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed."})


class RequestPasswordResetAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_password_reset_email(serializer.validated_data["email"])
        return Response({"detail": "If that email exists, a reset link was sent."})


class ResetPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        raw = serializer.validated_data["token"]
        try:
            uidb64, token = raw.split(":", 1)
        except ValueError:
            return Response({"detail": "Invalid token format."}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_password_with_token(uidb64, token, serializer.validated_data["new_password"])
        if not user:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Password updated."})