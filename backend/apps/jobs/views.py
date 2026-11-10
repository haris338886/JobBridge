"""HTML + API views for jobs (public marketing + employer dashboard)."""
from __future__ import annotations

import logging
from datetime import timedelta

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView, View

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from common.mixins import RoleRequiredMixin

from .filters import JobFilter
from .models import Job, JobCategory
from .permissions import IsEmployerOrReadOnly
from .serializers import (
    JobCategorySerializer,
    JobCreateUpdateSerializer,
    JobDetailSerializer,
    JobListSerializer,
)
from .services import featured_jobs, increment_views, list_active_jobs

logger = logging.getLogger(__name__)


# ======================================================================
# HTML — Public marketing pages
# ======================================================================
class MarketingIndexView(TemplateView):
    template_name = "marketing/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured_jobs"] = featured_jobs(limit=6)
        ctx["total_jobs"] = Job.objects.filter(status="active").count()
        return ctx


class MarketingJobListView(ListView):
    template_name = "marketing/job-list.html"
    context_object_name = "jobs"
    paginate_by = 12

    def get_queryset(self):
        return list_active_jobs(
            search=self.request.GET.get("q", ""),
            location=self.request.GET.get("location", ""),
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = JobCategory.objects.all()
        return ctx


class MarketingJobDetailView(DetailView):
    template_name = "marketing/job-detail.html"
    model = Job
    context_object_name = "job"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Job.objects.select_related("company", "category")

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        increment_views(self.object)
        return response


class AboutView(TemplateView):
    template_name = "marketing/about.html"


class ContactView(TemplateView):
    template_name = "marketing/contact.html"

    def post(self, request):
        messages.success(request, "Thanks for your message — we'll be in touch.")
        return redirect("marketing:contact")


class CareersView(TemplateView):
    template_name = "marketing/careers.html"


class PrivacyView(TemplateView):
    template_name = "legal/privacy.html"


class TermsView(TemplateView):
    template_name = "legal/terms.html"


# ======================================================================
# HTML — Employer dashboard
# ======================================================================
class EmployerDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "employer/dashboard.html"
    required_roles = ("employer",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.applications.models import Application
        from apps.interviews.models import Interview

        qs = Job.objects.filter(employer=self.request.user)
        ctx["active_jobs_count"] = qs.filter(status="active").count()
        ctx["applicants_count"] = (
            Application.objects.filter(job__employer=self.request.user).count()
        )
        ctx["shortlisted_count"] = (
            Application.objects.filter(
                job__employer=self.request.user, status="shortlisted",
            ).count()
        )
        ctx["interviews_count"] = (
            Interview.objects.filter(
                application__job__employer=self.request.user,
            ).count()
        )
        ctx["recent_applicants"] = (
            Application.objects
            .filter(job__employer=self.request.user)
            .select_related("candidate__user", "job")
            .order_by("-created_at")[:5]
        )
        return ctx


class EmployerManageJobsView(RoleRequiredMixin, ListView):
    template_name = "employer/manage-jobs.html"
    context_object_name = "jobs"
    paginate_by = 12
    required_roles = ("employer",)

    def get_queryset(self):
        return (
            Job.objects.filter(employer=self.request.user)
            .select_related("company", "category")
            .order_by("-created_at")
        )


class EmployerCreateJobView(RoleRequiredMixin, View):
    template_name = "employer/create-job.html"
    required_roles = ("employer",)

    def get(self, request):
        return render(request, self.template_name, {
            "categories": JobCategory.objects.all(),
        })

    def post(self, request):
        from apps.companies.models import Company

        company = request.user.companies.first()
        if not company:
            company = Company.objects.create(
                owner=request.user,
                name=f"{request.user.get_full_name() or request.user.email}'s Company",
            )

        serializer = JobCreateUpdateSerializer(
            data=request.POST, context={"request": request},
        )
        if serializer.is_valid():
            try:
                serializer.save(company=company)
                messages.success(request, "Job posted!")
                return redirect("employers:manage_jobs")
            except Exception as exc:  # noqa: BLE001
                logger.exception("Job save failed")
                messages.error(request, f"Save failed: {exc}")
        else:
            logger.warning("Job post validation errors: %s", serializer.errors)
            error_summary = "; ".join(
                f"{field}: {errs!s}"
                for field, errs in serializer.errors.items()
            )
            messages.error(request, f"Could not post the job. {error_summary}")

        return render(request, self.template_name, {
            "categories": JobCategory.objects.all(),
            "errors": serializer.errors,
            **request.POST,
        })


class EmployerEditJobView(RoleRequiredMixin, View):
    template_name = "employer/edit-job.html"
    required_roles = ("employer",)

    def _get_job(self, request, pk):
        return get_object_or_404(Job, pk=pk, employer=request.user)

    def get(self, request, pk):
        job = self._get_job(request, pk)
        return render(request, self.template_name, {
            "job": job,
            "categories": JobCategory.objects.all(),
        })

    def post(self, request, pk):
        job = self._get_job(request, pk)
        serializer = JobCreateUpdateSerializer(
            job, data=request.POST, partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Job updated.")
            return redirect("employers:manage_jobs")
        return render(request, self.template_name, {
            "job": job,
            "categories": JobCategory.objects.all(),
            "errors": serializer.errors,
        })


class EmployerDeleteJobView(RoleRequiredMixin, View):
    required_roles = ("employer",)

    def get(self, request, pk):
        Job.objects.filter(pk=pk, employer=request.user).delete()
        messages.success(request, "Job deleted.")
        return redirect("employers:manage_jobs")

    def post(self, request, pk):
        Job.objects.filter(pk=pk, employer=request.user).delete()
        messages.success(request, "Job deleted.")
        return redirect("employers:manage_jobs")


class EmployerCompanyView(RoleRequiredMixin, TemplateView):
    template_name = "employer/company.html"
    required_roles = ("employer",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["company"] = self.request.user.companies.first()
        return ctx

    def post(self, request):
        from apps.companies.models import Company

        company = request.user.companies.first()
        if not company:
            company = Company.objects.create(owner=request.user, name="My Company")
        for field in ["name", "website", "industry", "size", "description", "location"]:
            if field in request.POST:
                setattr(company, field, request.POST[field])
        if "logo" in request.FILES:
            company.logo = request.FILES["logo"]
        company.save()
        messages.success(request, "Company updated.")
        return redirect("employers:company")


class EmployerApplicantsView(RoleRequiredMixin, TemplateView):
    template_name = "employer/applicants.html"
    required_roles = ("employer",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.applications.models import Application

        ctx["applications"] = (
            Application.objects
            .filter(job__employer=self.request.user)
            .select_related("candidate__user", "job")
            .order_by("-created_at")
        )
        return ctx


class EmployerApplicantDetailView(RoleRequiredMixin, TemplateView):
    template_name = "employer/applicant-details.html"
    required_roles = ("employer",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.applications.models import Application
        from apps.interviews.models import Interview

        application = get_object_or_404(
            Application.objects.select_related("candidate__user", "job"),
            pk=self.kwargs["pk"],
            job__employer=self.request.user,
        )
        ctx["application"] = application
        ctx["interview"] = Interview.objects.filter(application=application).first()
        return ctx

    def post(self, request, *args, **kwargs):
        from apps.applications.models import Application
        from apps.interviews.models import Interview

        app = get_object_or_404(
            Application,
            pk=self.kwargs["pk"],
            job__employer=request.user,
        )
        action = (request.POST.get("action") or "").strip()
        logger.warning(
            "[APPLICANT ACTION] app=%s action=%r user=%s",
            app.pk, action, request.user.email,
        )

        if action == "shortlist":
            app.status = "shortlisted"
            app.save(update_fields=["status"])
            messages.success(request, "Applicant shortlisted.")

        elif action == "reject":
            app.status = "rejected"
            app.save(update_fields=["status"])
            messages.success(request, "Applicant rejected.")

        elif action == "schedule_interview":
            try:
                # Use filter().first() instead of get_or_create() to avoid
                # MultipleObjectsReturned on legacy duplicate rows.
                interview = Interview.objects.filter(application=app).first()
                if interview is None:
                    interview = Interview.objects.create(
                        application=app,
                        scheduled_at=timezone.now() + timedelta(days=7),
                        interview_type="video",
                        status="scheduled",
                    )
                if app.status != "interview":
                    app.status = "interview"
                    app.save(update_fields=["status"])

                logger.warning(
                    "[INTERVIEW CREATED] app=%s id=%s scheduled_at=%s",
                    app.pk, interview.pk, interview.scheduled_at,
                )
                messages.success(
                    request,
                    f"Interview scheduled for "
                    f"{interview.scheduled_at:%Y-%m-%d %H:%M}.",
                )
            except Exception as exc:  # noqa: BLE001
                logger.exception("[INTERVIEW FAILED] app=%s: %s", app.pk, exc)
                messages.error(request, f"Could not schedule interview: {exc}")

        else:
            logger.warning("[APPLICANT ACTION] unknown action=%r", action)
            messages.error(request, f"Unknown action: {action!r}")

        return redirect("employers:applicant_details", pk=app.pk)


class EmployerShortlistedView(RoleRequiredMixin, TemplateView):
    template_name = "employer/shortlisted.html"
    required_roles = ("employer",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.applications.models import Application

        ctx["shortlisted"] = Application.objects.filter(
            job__employer=self.request.user, status="shortlisted",
        ).select_related("candidate__user", "job")
        return ctx


class EmployerInterviewsView(RoleRequiredMixin, TemplateView):
    template_name = "employer/interviews.html"
    required_roles = ("employer",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.interviews.models import Interview

        ctx["interviews"] = (
            Interview.objects
            .filter(application__job__employer=self.request.user)
            .select_related(
                "application__candidate__user",
                "application__job",
            )
            .order_by("-scheduled_at")
        )
        return ctx


class EmployerNotificationsView(RoleRequiredMixin, TemplateView):
    template_name = "employer/notifications.html"
    required_roles = ("employer",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.notifications.models import Notification

        ctx["notifications"] = Notification.objects.filter(
            user=self.request.user,
        ).order_by("-created_at")[:50]
        return ctx

    def post(self, request):
        from apps.notifications.services import mark_all_read

        mark_all_read(request.user)
        messages.success(request, "All notifications marked as read.")
        return redirect("employers:notifications")


class EmployerSettingsView(RoleRequiredMixin, TemplateView):
    template_name = "employer/settings.html"
    required_roles = ("employer",)


# ======================================================================
# API — DRF
# ======================================================================
class JobViewSet(ModelViewSet):
    queryset = Job.objects.select_related("company", "category", "employer")
    permission_classes = [IsEmployerOrReadOnly]
    filterset_class = JobFilter
    search_fields = ["title", "description", "location", "company__name"]
    ordering_fields = ["created_at", "salary_min", "views_count"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return JobListSerializer
        if self.action in ("create", "update", "partial_update"):
            return JobCreateUpdateSerializer
        return JobDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        increment_views(instance)
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=["post"],
            permission_classes=[permissions.IsAuthenticated])
    def save(self, request, pk=None):
        job = self.get_object()
        from apps.candidates.models import SavedJob

        candidate = getattr(request.user, "candidate_profile", None)
        if not candidate:
            return Response(
                {"detail": "Only candidates can save jobs."},
                status=status.HTTP_403_FORBIDDEN,
            )
        SavedJob.objects.get_or_create(candidate=candidate, job=job)
        return Response({"detail": "Job saved."})


class JobCategoryViewSet(ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"