"""
Production settings for JobBridge.

Requires these env vars:
    DJANGO_SECRET_KEY, DJANGO_ALLOWED_HOSTS, DATABASE_URL,
    REDIS_URL, EMAIL_*, CORS_ALLOWED_ORIGINS
"""
from .base import *  # noqa: F401,F403

# ------------------------------------------------------------
# Core
# ------------------------------------------------------------
DEBUG = False
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")  # noqa: F405

# ------------------------------------------------------------
# Security hardening
# ------------------------------------------------------------
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)  # noqa: F405
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)  # noqa: F405
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)  # noqa: F405
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)        # noqa: F405
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ------------------------------------------------------------
# Email — SMTP required
# ------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# ------------------------------------------------------------
# Static — whitenoise manifest
# ------------------------------------------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MAX_AGE = 31536000
WHITENOISE_COMPRESS_OFFLINE = True

# ------------------------------------------------------------
# CORS — explicit list required
# ------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS")  # noqa: F405
CSRF_TRUSTED_ORIGINS = env("CORS_ALLOWED_ORIGINS")  # noqa: F405

# ------------------------------------------------------------
# Logging — file-based (container-friendly: stdout)
# ------------------------------------------------------------
LOGGING["root"]["level"] = "INFO"                # noqa: F405
LOGGING["loggers"]["django"]["level"] = "INFO"   # noqa: F405
LOGGING["loggers"]["apps"]["level"] = "INFO"     # noqa: F405

# ------------------------------------------------------------
# Sentry (optional)
# ------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN", default="")  # noqa: F405
if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[DjangoIntegration()],
            traces_sample_rate=0.1,
            send_default_pii=False,
        )
    except ImportError:
        pass