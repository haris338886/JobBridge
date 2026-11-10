"""URLs for interviews."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InterviewViewSet

router = DefaultRouter()
router.register("", InterviewViewSet, basename="interview")

app_name = "interviews"
urlpatterns = [path("api/", include(router.urls))]