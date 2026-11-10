"""API views for reviews."""
from rest_framework import permissions, viewsets

from .models import Review
from .permissions import IsReviewOwner
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsReviewOwner]

    def get_queryset(self):
        return Review.objects.select_related("company", "candidate__user")

    def perform_create(self, serializer):
        serializer.save()