import logging
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

@shared_task
def send_email_notification(user_id, message):
    try:
        user = User.objects.get(pk=user_id)
        send_mail(
            'Notification',
            message,
            'admin_project_management@yopmail.com',
            [user.email],
            fail_silently=False,
        )
        logger.info(f"Email notification sent to {user.email} with message: {message}")
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist.")
    except Exception as e:
        logger.error(f"Failed to send email notification: {str(e)}")
