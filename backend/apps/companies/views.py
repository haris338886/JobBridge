"""API views for companies."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Company
from .permissions import IsCompanyOwner
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwner]
    lookup_field = "slug"
    search_fields = ["name", "industry", "location"]
    filterset_fields = ["industry", "size"]