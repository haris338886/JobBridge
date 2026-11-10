"""URLs for reviews."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet

router = DefaultRouter()
router.register("", ReviewViewSet, basename="review")

app_name = "reviews"
urlpatterns = [path("api/", include(router.urls))]