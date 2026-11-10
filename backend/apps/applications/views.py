"""API views for applications."""
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Application
from .permissions import IsApplicationCandidate, IsApplicationEmployer
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationListSerializer,
    ApplicationUpdateSerializer,
)
from .services import create_application, update_status


class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Application.objects.select_related(
            "job__company", "candidate__user",
        )
        if user.is_employer:
            return qs.filter(job__employer=user)
        if user.is_candidate:
            return qs.filter(candidate__user=user)
        return qs.none()

    def get_serializer_class(self):
        if self.action == "create":
            return ApplicationCreateSerializer
        if self.action in ("update", "partial_update", "set_status"):
            return ApplicationUpdateSerializer
        return ApplicationListSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom create so the response always contains the persisted
        Application (including its ``id``), regardless of the fact
        that ``perform_create`` delegates to ``services.create_application``.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = serializer.validated_data["job"]
        candidate = getattr(request.user, "candidate_profile", None)
        if candidate is None:
            return Response(
                {"detail": "You must be a candidate to apply."},
                status=status.HTTP_403_FORBIDDEN,
            )

        cover_letter = serializer.validated_data.get("cover_letter", "")
        resume = serializer.validated_data.get("resume")

        application = create_application(
            job=job,
            candidate=candidate,
            cover_letter=cover_letter,
            resume=resume,
        )

        response_serializer = ApplicationListSerializer(
            application, context=self.get_serializer_context(),
        )
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        # Kept for compatibility; ``create`` above handles creation.
        job = serializer.validated_data["job"]
        candidate = self.request.user.candidate_profile
        cover = serializer.validated_data.get("cover_letter", "")
        resume = serializer.validated_data.get("resume")
        application = create_application(
            job=job, candidate=candidate,
            cover_letter=cover, resume=resume,
        )
        serializer.instance = application

    @action(detail=True, methods=["post"],
            permission_classes=[permissions.IsAuthenticated, IsApplicationEmployer])
    def set_status(self, request, pk=None):
        app = self.get_object()
        new_status = request.data.get("status")
        notes = request.data.get("notes", "")
        valid = dict(app._meta.get_field("status").choices)
        if new_status not in valid:
            return Response(
                {"detail": "Invalid status."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        update_status(app, new_status, notes)
        return Response({"detail": "Status updated."})

    @action(detail=True, methods=["post"],
            permission_classes=[permissions.IsAuthenticated, IsApplicationCandidate])
    def withdraw(self, request, pk=None):
        app = self.get_object()
        app.status = "withdrawn"
        app.save(update_fields=["status"])
        return Response({"detail": "Application withdrawn."})