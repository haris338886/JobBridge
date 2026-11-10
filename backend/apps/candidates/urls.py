"""URLs for candidates."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# HTML (no tuple — app_name at the bottom handles the namespace)
html_patterns = [
    path("", views.CandidateDashboardView.as_view(), name="dashboard"),
    path("profile/", views.CandidateProfileView.as_view(), name="profile"),
    path("applications/", views.CandidateApplicationsView.as_view(), name="applications"),
    path("applications/<int:pk>/", views.CandidateApplicationDetailView.as_view(), name="application_detail"),
    path("saved-jobs/", views.CandidateSavedJobsView.as_view(), name="saved_jobs"),
    path("saved-jobs/<int:pk>/remove/", views.CandidateRemoveSavedView.as_view(), name="remove_saved"),
    path("resume/", views.CandidateResumeView.as_view(), name="resume"),
    path("education/", views.CandidateEducationView.as_view(), name="education"),
    path("education/delete/<int:pk>/", views.CandidateDeleteEducationView.as_view(), name="delete_education"),
    path("experience/", views.CandidateExperienceView.as_view(), name="experience"),
    path("experience/delete/<int:pk>/", views.CandidateDeleteExperienceView.as_view(), name="delete_experience"),
    path("skills/", views.CandidateSkillsView.as_view(), name="skills"),
    path("skills/<int:pk>/delete/", views.CandidateDeleteSkillView.as_view(), name="delete_skill"),
    path("notifications/", views.CandidateNotificationsView.as_view(), name="notifications"),
    path("settings/", views.CandidateSettingsView.as_view(), name="settings"),
]

# API
router = DefaultRouter()
router.register("profile", views.CandidateViewSet, basename="profile")
router.register("education", views.EducationViewSet, basename="education")
router.register("experience", views.ExperienceViewSet, basename="experience")
router.register("skills", views.SkillViewSet, basename="skill")
router.register("saved", views.SavedJobViewSet, basename="saved")

app_name = "candidates"

urlpatterns = [
    path("", include(html_patterns)),
    path("api/", include(router.urls)),
]