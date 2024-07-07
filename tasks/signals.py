from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task
from notifications.models import Notification

@receiver(post_save, sender=Task)
def task_created_or_updated(sender, instance, created, **kwargs):
    if created:
        action = 'created'
        message = f'Task "{instance.name}" has been created.'
    else:
        action = 'updated'
        message = f'Task "{instance.name}" has been updated.'
    
    Notification.objects.create(user=instance.assigned_to, message=message)
    
    # Send email notification using Celery
    from notifications.tasks import send_email_notification
    send_email_notification.delay(instance.assigned_to.id, message)