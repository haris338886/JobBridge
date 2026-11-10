"""
JobBridge root URL configuration.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


# ============================================================
# URL patterns
# ============================================================
urlpatterns = [
    path("admin/", admin.site.urls),

    # Public site + employer dashboard + jobs API
    path("", include("apps.jobs.urls")),

    # Auth
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),

    # App namespaces
    path("candidate/", include("apps.candidates.urls", namespace="candidates")),
    path("applications/", include("apps.applications.urls", namespace="applications")),
    path("interviews/", include("apps.interviews.urls", namespace="interviews")),
    path("notifications/", include("apps.notifications.urls", namespace="notifications")),
    path("reviews/", include("apps.reviews.urls", namespace="reviews")),
    path("companies/", include("apps.companies.urls", namespace="companies")),
    path("admin-panel/", include("apps.admin_panel.urls", namespace="admin_panel")),
]

# Static + media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# ============================================================
# Custom error handlers
# ------------------------------------------------------------
# These MUST live at module level — Django imports this module
# and looks up `handler404`, `handler403`, `handler500` by name.
# Put them AFTER `urlpatterns` so any local imports / variables
# they rely on are already defined.
# ============================================================

def handler404(request, exception):
    """Custom 404 page — rendered with full context."""
    return render(request, "errors/404.html", status=404)


def handler403(request, exception):
    """Custom 403 page — rendered with full context."""
    return render(request, "errors/403.html", status=403)


def handler500(request):
    """Custom 500 page.

    NOTE: Django calls this WITHOUT a RequestContext, so `errors/500.html`
    must not rely on context processors (we already made it self-contained).
    """
    return render(request, "errors/500.html", status=500)