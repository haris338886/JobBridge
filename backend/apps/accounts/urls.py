"""URL configuration for accounts (HTML + API)."""
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    # ---------- HTML views ----------
    path("login/",           views.LoginView.as_view(),                name="login"),
    path("logout/",          views.logout_view,                        name="logout"),
    path("register/",        views.RegisterChoiceView.as_view(),       name="register"),
    path("register/candidate/", views.RegisterCandidateView.as_view(), name="register_candidate"),
    path("register/employer/",  views.RegisterEmployerView.as_view(),  name="register_employer"),

    path("forgot-password/", views.ForgotPasswordView.as_view(),       name="forgot_password"),
    path(
        "reset-password/<uidb64>/<token>/",
        views.ResetPasswordView.as_view(),
        name="reset_password_confirm",
    ),
    path(
        "verify-email/<uidb64>/<token>/",
        views.VerifyEmailView.as_view(),
        name="verify_email_confirm",
    ),
    path("change-password/", views.ChangePasswordView.as_view(),       name="change_password"),

    # ---------- API views ----------
    path("api/register/",        views.RegisterAPIView.as_view(),        name="api_register"),
    path("api/login/",           views.LoginAPIView.as_view(),           name="api_login"),
    path("api/logout/",          views.LogoutAPIView.as_view(),          name="api_logout"),
    path("api/me/",              views.MeAPIView.as_view(),              name="api_me"),
    path("api/change-password/", views.ChangePasswordAPIView.as_view(),  name="api_change_password"),
    path("api/password-reset/",  views.RequestPasswordResetAPIView.as_view(), name="api_password_reset"),
    path("api/password-reset/confirm/", views.ResetPasswordAPIView.as_view(), name="api_password_reset_confirm"),
    path("api/token/refresh/",   __import__("rest_framework_simplejwt.views", fromlist=["TokenRefreshView"]).TokenRefreshView.as_view(), name="api_token_refresh"),
]