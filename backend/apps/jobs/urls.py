"""
URL configuration for jobs app.

Exposes three top-level namespaces:
  - `marketing`  → public marketing pages
  - `employers`  → employer dashboard
  - `jobs_api`   → DRF API routes

`config/urls.py` mounts the whole module at "/".
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# ------------------------------------------------------------
# Public marketing pages (namespace = "marketing")
# ------------------------------------------------------------
marketing_patterns = [
    path("", views.MarketingIndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("careers/", views.CareersView.as_view(), name="careers"),
    path("jobs/", views.MarketingJobListView.as_view(), name="job_list"),
    path("jobs/<slug:slug>/", views.MarketingJobDetailView.as_view(), name="job_detail"),
    path("legal/privacy/", views.PrivacyView.as_view(), name="privacy"),
    path("legal/terms/", views.TermsView.as_view(), name="terms"),
]

# ------------------------------------------------------------
# Employer dashboard (namespace = "employers")
# ------------------------------------------------------------
employer_patterns = [
    path("", views.EmployerDashboardView.as_view(), name="dashboard"),
    path("company/", views.EmployerCompanyView.as_view(), name="company"),
    path("jobs/create/", views.EmployerCreateJobView.as_view(), name="create_job"),
    path("jobs/", views.EmployerManageJobsView.as_view(), name="manage_jobs"),
    path("jobs/<int:pk>/edit/", views.EmployerEditJobView.as_view(), name="edit_job"),
    path("jobs/<int:pk>/delete/", views.EmployerDeleteJobView.as_view(), name="delete_job"),
    path("applicants/", views.EmployerApplicantsView.as_view(), name="applicants"),
    path("applicants/<int:pk>/", views.EmployerApplicantDetailView.as_view(), name="applicant_details"),
    path("shortlisted/", views.EmployerShortlistedView.as_view(), name="shortlisted"),
    path("interviews/", views.EmployerInterviewsView.as_view(), name="interviews"),
    path("notifications/", views.EmployerNotificationsView.as_view(), name="notifications"),
    path("settings/", views.EmployerSettingsView.as_view(), name="settings"),
]

# ------------------------------------------------------------
# API (namespace = "jobs_api")
# ------------------------------------------------------------
router = DefaultRouter()
router.register("categories", views.JobCategoryViewSet, basename="category")
router.register("", views.JobViewSet, basename="job")

# ------------------------------------------------------------
# NO `app_name = "jobs"` here — we register each namespace explicitly
# so that `{% url 'marketing:index' %}` resolves at the top level.
# ------------------------------------------------------------
urlpatterns = [
    path("", include((marketing_patterns, "marketing"), namespace="marketing")),
    path("employer/", include((employer_patterns, "employers"), namespace="employers")),
    path("api/", include((router.urls, "jobs_api"), namespace="jobs_api")),
]