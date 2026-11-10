"""Admin panel views (staff only)."""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView


class StaffRequiredMixin(UserPassesTestMixin):
    """Only staff / admin users may access."""

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_staff or getattr(self.request.user, "is_admin_role", False)
        )


class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.accounts.models import User
        from apps.jobs.models import Job
        from apps.applications.models import Application
        ctx["total_users"] = User.objects.count()
        ctx["total_jobs"] = Job.objects.count()
        ctx["total_applications"] = Application.objects.count()
        ctx["pending_feedback"] = 0
        ctx["recent_activity"] = []
        return ctx


class UsersView(StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/users.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.accounts.models import User
        ctx["users"] = User.objects.all().order_by("-date_joined")
        return ctx


class CandidatesView(StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/candidates.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.candidates.models import Candidate
        ctx["candidates"] = Candidate.objects.select_related("user")
        return ctx


class EmployersView(StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/employers.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.accounts.models import User
        ctx["employers"] = User.objects.filter(role="employer").select_related()
        return ctx


class CompaniesView(StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/companies.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.companies.models import Company
        ctx["companies"] = Company.objects.all()
        return ctx


class JobsView(StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/jobs.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.jobs.models import Job
        ctx["jobs"] = Job.objects.select_related("company").order_by("-created_at")
        return ctx


class ApplicationsView(StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/applications.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.applications.models import Application
        ctx["applications"] = Application.objects.select_related(
            "job__company", "candidate__user"
        ).order_by("-created_at")
        return ctx


class CategoriesView(StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/categories.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.jobs.models import JobCategory
        ctx["categories"] = JobCategory.objects.all()
        return ctx


class ReportsView(StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/reports.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["new_users_30d"] = 0
        ctx["new_jobs_30d"] = 0
        ctx["applications_30d"] = 0
        ctx["hire_rate"] = 0
        return ctx


class FeedbackView(StaffRequiredMixin, TemplateView):
    template_name = "admin_panel/feedback.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["feedback_list"] = []
        return ctx