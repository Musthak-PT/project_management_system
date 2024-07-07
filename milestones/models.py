from django.db import models
from projects.models import Project

# Create your models here.
class Milestone(models.Model):
    project       = models.ForeignKey(Project, related_name='milestones', on_delete=models.CASCADE)
    name          = models.CharField(max_length=255)
    due_date      = models.DateTimeField()
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)