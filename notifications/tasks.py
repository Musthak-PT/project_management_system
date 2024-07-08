from celery import shared_task
from django.core.mail import send_mail
from project_management import settings
import logging

logger = logging.getLogger('django')

@shared_task
def send_email_notification(email, subject, message):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}")