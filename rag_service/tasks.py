import logging
from datetime import timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore

logger = logging.getLogger(__name__)


def delete_old_chat_history():
    """
    Delete chat history older than 30 days.
    This task runs daily at midnight.
    """
    from .models import ChatHistory
    
    cutoff_date = timezone.now() - timedelta(days=30)
    old_records = ChatHistory.objects.filter(created_at__lt=cutoff_date)
    count = old_records.count()
    
    if count > 0:
        old_records.delete()
        logger.info(f"Deleted {count} chat history records older than 30 days")
    else:
        logger.info("No old chat history records to delete")


def start_scheduler():
    """Initialize and start the background scheduler."""
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # Schedule the cleanup task to run daily at midnight
    scheduler.add_job(
        delete_old_chat_history,
        trigger=CronTrigger(hour=0, minute=0),  # Run at midnight
        id="delete_old_chat_history",
        max_instances=1,
        replace_existing=True,
    )
    
    logger.info("Starting background scheduler...")
    scheduler.start()
    logger.info("Background scheduler started. Chat history cleanup scheduled for midnight daily.")
