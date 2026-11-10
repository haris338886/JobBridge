"""Project-wide constants."""
from django.utils.translation import gettext_lazy as _


class Role:
    CANDIDATE = "candidate"
    EMPLOYER = "employer"
    ADMIN = "admin"

    CHOICES = [
        (CANDIDATE, _("Candidate")),
        (EMPLOYER, _("Employer")),
        (ADMIN, _("Administrator")),
    ]


class JobType:
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    REMOTE = "remote"

    CHOICES = [
        (FULL_TIME, _("Full Time")),
        (PART_TIME, _("Part Time")),
        (CONTRACT, _("Contract")),
        (INTERNSHIP, _("Internship")),
        (REMOTE, _("Remote")),
    ]


class JobStatus:
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"

    CHOICES = [
        (DRAFT, _("Draft")),
        (ACTIVE, _("Active")),
        (CLOSED, _("Closed")),
        (ARCHIVED, _("Archived")),
    ]


class ApplicationStatus:
    APPLIED = "applied"
    REVIEWING = "reviewing"
    SHORTLISTED = "shortlisted"
    INTERVIEW = "interview"
    OFFERED = "offered"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

    CHOICES = [
        (APPLIED, _("Applied")),
        (REVIEWING, _("Reviewing")),
        (SHORTLISTED, _("Shortlisted")),
        (INTERVIEW, _("Interview")),
        (OFFERED, _("Offered")),
        (HIRED, _("Hired")),
        (REJECTED, _("Rejected")),
        (WITHDRAWN, _("Withdrawn")),
    ]


class InterviewType:
    PHONE = "phone"
    VIDEO = "video"
    IN_PERSON = "in_person"
    TECHNICAL = "technical"
    HR = "hr"

    CHOICES = [
        (PHONE, _("Phone")),
        (VIDEO, _("Video Call")),
        (IN_PERSON, _("In Person")),
        (TECHNICAL, _("Technical")),
        (HR, _("HR Round")),
    ]


class InterviewStatus:
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"
    NO_SHOW = "no_show"

    CHOICES = [
        (SCHEDULED, _("Scheduled")),
        (COMPLETED, _("Completed")),
        (CANCELLED, _("Cancelled")),
        (RESCHEDULED, _("Rescheduled")),
        (NO_SHOW, _("No Show")),
    ]


class NotificationType:
    APPLICATION = "application"
    INTERVIEW = "interview"
    MESSAGE = "message"
    SYSTEM = "system"
    OFFER = "offer"

    CHOICES = [
        (APPLICATION, _("Application Update")),
        (INTERVIEW, _("Interview Update")),
        (MESSAGE, _("Message")),
        (SYSTEM, _("System")),
        (OFFER, _("Offer")),
    ]


PAGE_SIZE = 20
MAX_RESUME_SIZE_MB = 5
MAX_AVATAR_SIZE_MB = 2