from django.contrib.auth.models import AbstractUser
from django.db import models

 #User model with Roles :admin, manager and member
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('member', 'Member'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)