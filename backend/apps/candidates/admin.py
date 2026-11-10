"""Admin for candidates."""
from django.contrib import admin

from .models import Candidate, Education, Experience, SavedJob, Skill


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("user", "headline", "location", "years_of_experience", "is_open_to_work")
    search_fields = ("user__email", "user__first_name", "user__last_name", "headline")
    list_filter = ("is_open_to_work",)
    inlines = [EducationInline, ExperienceInline, SkillInline]
    raw_id_fields = ("user",)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job", "created_at")
    raw_id_fields = ("candidate", "job")