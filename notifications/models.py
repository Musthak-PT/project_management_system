from django.db import models
from users.models import User

# Create your models here.
class Notification(models.Model):
    user          = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message       = models.CharField(max_length=255)
    created_at    = models.DateTimeField(auto_now_add=True)
    is_read       = models.BooleanField(default=False)