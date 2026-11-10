"""URLs for admin_panel."""
from django.urls import path

from . import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("users/", views.UsersView.as_view(), name="users"),
    path("users/<int:pk>/", views.UsersView.as_view(), name="user_detail"),
    path("candidates/", views.CandidatesView.as_view(), name="candidates"),
    path("candidates/<int:pk>/", views.CandidatesView.as_view(), name="candidate_detail"),
    path("employers/", views.EmployersView.as_view(), name="employers"),
    path("employers/<int:pk>/", views.EmployersView.as_view(), name="employer_detail"),
    path("companies/", views.CompaniesView.as_view(), name="companies"),
    path("companies/<int:pk>/", views.CompaniesView.as_view(), name="company_detail"),
    path("jobs/", views.JobsView.as_view(), name="jobs"),
    path("jobs/<int:pk>/", views.JobsView.as_view(), name="job_detail"),
    path("applications/", views.ApplicationsView.as_view(), name="applications"),
    path("applications/<int:pk>/", views.ApplicationsView.as_view(), name="application_detail"),
    path("categories/", views.CategoriesView.as_view(), name="categories"),
    path("categories/create/", views.CategoriesView.as_view(), name="create_category"),
    path("categories/<int:pk>/edit/", views.CategoriesView.as_view(), name="edit_category"),
    path("categories/<int:pk>/delete/", views.CategoriesView.as_view(), name="delete_category"),
    path("reports/", views.ReportsView.as_view(), name="reports"),
    path("reports/export/users/", views.ReportsView.as_view(), name="export_users"),
    path("reports/export/jobs/", views.ReportsView.as_view(), name="export_jobs"),
    path("reports/export/applications/", views.ReportsView.as_view(), name="export_applications"),
    path("feedback/", views.FeedbackView.as_view(), name="feedback"),
]