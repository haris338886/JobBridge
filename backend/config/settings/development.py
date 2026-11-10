"""
Development settings for JobBridge.

Import before running:
    export DJANGO_SETTINGS_MODULE=config.settings.development
"""
from .base import *  # noqa: F401,F403

# ------------------------------------------------------------
# Debug
# ------------------------------------------------------------
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ------------------------------------------------------------
# Database — SQLite for local dev unless DATABASE_URL is set
# ------------------------------------------------------------
# (inherited from base.py; DATABASE_URL takes precedence)

# ------------------------------------------------------------
# Email — console backend
# ------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ------------------------------------------------------------
# Static — plain storage (no manifest, easier for dev)
# ------------------------------------------------------------
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# ------------------------------------------------------------
# CORS — permissive in dev
# ------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://localhost:8000",
    "https://127.0.0.1:8000",
]

# ------------------------------------------------------------
# Logging — DEBUG level
# ------------------------------------------------------------
LOGGING["root"]["level"] = "DEBUG"           # noqa: F405
LOGGING["loggers"]["django"]["level"] = "INFO"   # noqa: F405
LOGGING["loggers"]["apps"]["level"] = "DEBUG"    # noqa: F405

# ------------------------------------------------------------
# Debug toolbar (enable if installed)
# ------------------------------------------------------------
try:
    import debug_toolbar  # noqa: F401
    INSTALLED_APPS += ["debug_toolbar"]                      # noqa: F405
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
    INTERNAL_IPS = ["127.0.0.1", "localhost"]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
    }
except ImportError:
    pass