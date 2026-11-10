"""URLs for applications."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ApplicationViewSet

router = DefaultRouter()
router.register("", ApplicationViewSet, basename="application")

app_name = "applications"
urlpatterns = [path("api/", include(router.urls))]