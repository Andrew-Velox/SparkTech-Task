import logging
from threading import Thread
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)


def send_verification_email_task(user_email, username):
    """Send verification email after user signup using HTML template."""
    def _send_email():
        try:
            subject = "Welcome to RAG Chatbot"
            
            # Render HTML template
            html_message = render_to_string('welcome_email.html', {
                'username': username,
            })
            
            # Plain text fallback message
            message = f"Welcome {username}! Thank you for signing up for RAG Chatbot."
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Verification email sent to {user_email}")
        except Exception as e:
            logger.error(f"Failed to send verification email to {user_email}: {e}")
    
    # Run email sending in a background thread
    thread = Thread(target=_send_email)
    thread.start()
