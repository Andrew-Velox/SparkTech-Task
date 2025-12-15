import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserDocument

logger = logging.getLogger(__name__)


@receiver(post_save, sender=UserDocument)
def log_document_upload(sender, instance, created, **kwargs):
    """Log when a document is uploaded."""
    if created:
        logger.info(f"Document '{instance.title}' uploaded by user {instance.user_id}")

