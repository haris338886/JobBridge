"""Field validators shared across apps."""
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

MAX_RESUME_MB = 5
MAX_IMAGE_MB = 2

resume_validator = FileExtensionValidator(
    allowed_extensions=["pdf", "doc", "docx"],
    message="Resume must be a PDF or Word document.",
)


def validate_resume_size(value):
    if value.size > MAX_RESUME_MB * 1024 * 1024:
        raise ValidationError(f"Resume must be under {MAX_RESUME_MB} MB.")


def validate_image_size(value):
    if value.size > MAX_IMAGE_MB * 1024 * 1024:
        raise ValidationError(f"Image must be under {MAX_IMAGE_MB} MB.")