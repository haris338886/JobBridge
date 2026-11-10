"""Signal handlers for applications."""
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Application


@receiver(post_save, sender=Application)
def application_created(sender, instance, created, **kwargs):
    if created:
        pass  # notifications handled in services.create_application