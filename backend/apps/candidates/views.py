"""HTML + API views for candidates."""
from __future__ import annotations

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.mixins import RoleRequiredMixin

from .models import Candidate, Education, Experience, SavedJob, Skill
from .permissions import IsCandidate
from .serializers import (
    CandidateSerializer,
    EducationSerializer,
    ExperienceSerializer,
    SavedJobSerializer,
    SkillSerializer,
)
from .services import get_or_create_candidate


# ======================================================================
# HTML views (candidate dashboard)
# ======================================================================
class CandidateDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/dashboard.html"
    required_roles = ("candidate",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        candidate = get_or_create_candidate(self.request.user)
        from apps.applications.models import Application
        apps_qs = Application.objects.filter(candidate=candidate)
        ctx["applications_count"] = apps_qs.count()
        ctx["saved_jobs_count"] = candidate.saved_jobs.count()
        ctx["interviews_count"] = 0
        ctx["recent_applications"] = (
            apps_qs.select_related("job__company").order_by("-created_at")[:5]
        )
        return ctx


class CandidateProfileView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/profile.html"
    required_roles = ("candidate",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = get_or_create_candidate(self.request.user)
        return ctx

    def post(self, request):
        candidate = get_or_create_candidate(request.user)
        for field in ["headline", "phone", "location", "linkedin", "portfolio"]:
            if field in request.POST:
                setattr(candidate, field, request.POST[field])
        # Template uses `bio`, model uses `summary` — map them.
        if "bio" in request.POST:
            candidate.summary = request.POST["bio"]
        if "profile_image" in request.FILES:
            request.user.profile.avatar = request.FILES["profile_image"]
            request.user.profile.save()
        candidate.save()
        request.user.first_name = request.POST.get("first_name", request.user.first_name)
        request.user.last_name = request.POST.get("last_name", request.user.last_name)
        request.user.save(update_fields=["first_name", "last_name"])
        messages.success(request, "Profile updated.")
        return redirect("candidates:profile")


class CandidateApplicationsView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/applications.html"
    required_roles = ("candidate",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.applications.models import Application
        ctx["applications"] = (
            Application.objects
            .filter(candidate__user=self.request.user)
            .select_related("job__company")
            .order_by("-created_at")
        )
        return ctx


class CandidateApplicationDetailView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/application-detail.html"
    required_roles = ("candidate",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.applications.models import Application
        ctx["application"] = get_object_or_404(
            Application, pk=self.kwargs["pk"], candidate__user=self.request.user,
        )
        return ctx


class CandidateSavedJobsView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/saved-jobs.html"
    required_roles = ("candidate",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        candidate = get_or_create_candidate(self.request.user)
        ctx["saved_jobs"] = candidate.saved_jobs.select_related("job__company")
        return ctx


class CandidateRemoveSavedView(RoleRequiredMixin, View):
    required_roles = ("candidate",)

    def post(self, request, pk):
        SavedJob.objects.filter(pk=pk, candidate__user=request.user).delete()
        messages.success(request, "Removed from saved jobs.")
        return redirect("candidates:saved_jobs")


class CandidateResumeView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/resume.html"
    required_roles = ("candidate",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = get_or_create_candidate(self.request.user)
        return ctx

    def post(self, request):
        candidate = get_or_create_candidate(request.user)
        if "resume" in request.FILES:
            candidate.resume = request.FILES["resume"]
            candidate.save()
            messages.success(request, "Resume uploaded.")
        return redirect("candidates:resume")


class CandidateEducationView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/education.html"
    required_roles = ("candidate",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        candidate = get_or_create_candidate(self.request.user)
        ctx["education_list"] = candidate.education.all()
        return ctx

    def post(self, request):
        candidate = get_or_create_candidate(self.request.user)
        Education.objects.create(
            candidate=candidate,
            degree=request.POST.get("degree", "").strip(),
            institution=request.POST.get("institution", "").strip(),
            field_of_study=request.POST.get("field_of_study", "").strip(),
            start_year=request.POST.get("start_year") or None,
            end_year=request.POST.get("end_year") or None,
            description=request.POST.get("description", "").strip(),
        )
        messages.success(request, "Education added.")
        return redirect("candidates:education")


class CandidateDeleteEducationView(RoleRequiredMixin, View):
    required_roles = ("candidate",)

    def post(self, request, pk):
        Education.objects.filter(pk=pk, candidate__user=request.user).delete()
        messages.success(request, "Education removed.")
        return redirect("candidates:education")


class CandidateExperienceView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/experience.html"
    required_roles = ("candidate",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        candidate = get_or_create_candidate(self.request.user)
        ctx["experience_list"] = candidate.experience.all()
        return ctx

    def post(self, request):
        candidate = get_or_create_candidate(self.request.user)
        Experience.objects.create(
            candidate=candidate,
            title=request.POST.get("title", "").strip(),
            company=request.POST.get("company", "").strip(),
            location=request.POST.get("location", "").strip(),
            start_date=request.POST.get("start_date") or None,
            end_date=request.POST.get("end_date") or None,
            is_current="is_current" in request.POST,
            description=request.POST.get("description", "").strip(),
        )
        messages.success(request, "Experience added.")
        return redirect("candidates:experience")


class CandidateDeleteExperienceView(RoleRequiredMixin, View):
    required_roles = ("candidate",)

    def post(self, request, pk):
        Experience.objects.filter(pk=pk, candidate__user=request.user).delete()
        messages.success(request, "Experience removed.")
        return redirect("candidates:experience")


class CandidateSkillsView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/skills.html"
    required_roles = ("candidate",)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        candidate = get_or_create_candidate(self.request.user)
        ctx["skills"] = candidate.skills.all()
        return ctx

    def post(self, request):
        candidate = get_or_create_candidate(self.request.user)
        name = request.POST.get("skill", "").strip()
        if name:
            Skill.objects.get_or_create(candidate=candidate, name=name)
            messages.success(request, "Skill added.")
        return redirect("candidates:skills")


class CandidateDeleteSkillView(RoleRequiredMixin, View):
    required_roles = ("candidate",)

    def post(self, request, pk):
        Skill.objects.filter(pk=pk, candidate__user=request.user).delete()
        return redirect("candidates:skills")


class CandidateNotificationsView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/notifications.html"
    required_roles = ("candidate",)

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
        return redirect("candidates:notifications")


class CandidateSettingsView(RoleRequiredMixin, TemplateView):
    template_name = "candidate/settings.html"
    required_roles = ("candidate",)


# ======================================================================
# API
# ======================================================================
class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Candidate.objects.filter(user=self.request.user)

    def get_object(self):
        return get_or_create_candidate(self.request.user)

    @action(detail=False, methods=["post"])
    def add_skill(self, request):
        name = request.data.get("name", "").strip()
        if not name:
            return Response({"detail": "Skill name required."}, status=400)
        candidate = get_or_create_candidate(request.user)
        skill, _ = Skill.objects.get_or_create(candidate=candidate, name=name)
        return Response(SkillSerializer(skill).data, status=201)


class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return Education.objects.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(candidate=get_or_create_candidate(self.request.user))


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return Experience.objects.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(candidate=get_or_create_candidate(self.request.user))


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return Skill.objects.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(candidate=get_or_create_candidate(self.request.user))


class SavedJobViewSet(viewsets.ModelViewSet):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return SavedJob.objects.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(candidate=get_or_create_candidate(self.request.user))