from django.test import TestCase
from django.utils import timezone
from tasks.models import Task
from projects.models import Project
from users.models import User

class TaskModelTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name="Test Project", description="Test Project Description")
        self.user = User.objects.create(username="testuser")
        self.task_data = {
            "project": self.project,
            "name": "Test Task",
            "description": "Test Task Description",
            "assigned_to": self.user,
            "due_date": timezone.now(),
            "status": "Pending"
        }
        self.task = Task.objects.create(**self.task_data)

    def test_task_creation(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.project.name, "Test Project")
        self.assertEqual(task.assigned_to.username, "testuser")

    def test_task_deletion(self):
        task = Task.objects.get(id=self.task.id)
        task.delete()
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
