from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from notifications.models import Notification
from .tasks import send_email_notification

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    message = f'Task {instance.name} has been {action}.'
    
    # Create a Notification object
    Notification.objects.create(user=instance.user, message=message)
    
    # Send email notification using Celery
    send_email_notification.delay(instance.user.email, 'Task Notification', message)