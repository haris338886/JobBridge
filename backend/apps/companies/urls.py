"""URLs for companies (HTML mount is done from jobs app; API only here)."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet

router = DefaultRouter()
router.register("", CompanyViewSet, basename="company")

app_name = "companies"
urlpatterns = [path("api/", include(router.urls))]