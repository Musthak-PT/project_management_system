# tasks/tests/test_models.py
from django.test import TestCase
from django.utils import timezone
from tasks.models import Task
from projects.models import Project
from users.models import User

class TaskModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Test Project')
        self.user = User.objects.create(username='testuser')
        self.task = Task.objects.create(
            project=self.project,
            name='Test Task',
            description='Test Description',
            assigned_to=self.user,
            due_date=timezone.now(),
            status='Pending'
        )

    def test_task_creation(self):
        self.assertEqual(self.task.project.name, 'Test Project')
        self.assertEqual(self.task.name, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.assigned_to.username, 'testuser')
        self.assertTrue(isinstance(self.task.due_date, timezone.datetime))
        self.assertEqual(self.task.status, 'Pending')
