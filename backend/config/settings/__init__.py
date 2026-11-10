"""
Settings package entry.

Auto-selects the concrete settings module based on the
DJANGO_SETTINGS_MODULE env var. If it's not set, this module
falls back to ``base`` so ``manage.py`` always works.

Typical usage:
    DJANGO_SETTINGS_MODULE=config.settings.development
    DJANGO_SETTINGS_MODULE=config.settings.production

When Django imports ``config.settings``, this file runs first and
re-exports the correct module's namespace.
"""
import os

_ENV = os.environ.get("DJANGO_SETTINGS_MODULE", "")

if _ENV.endswith(".development"):
    from .development import *  # noqa: F401,F403
elif _ENV.endswith(".production"):
    from .production import *  # noqa: F401,F403
else:
    # Default: development-safe base
    from .base import *  # noqa: F401,F403