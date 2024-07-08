from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from tasks.models import Task
from projects.models import Project
from users.models import User
from tasks.serializers import CreateOrUpdateTaskSerializer, DeleteTasksApiRequestSerializer, AssignTasksSerializer

class TaskSerializerTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name="Test Project", description="Test Project Description")
        self.user = User.objects.create(username="testuser", role='manager')
        self.task_data = {
            "project": self.project.id,
            "name": "Test Task",
            "description": "Test Task Description",
            "assigned_to": self.user.id,
            "due_date": timezone.now(),
            "status": "Pending"
        }

    def test_create_task_serializer(self):
        serializer = CreateOrUpdateTaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.project.name, "Test Project")
        self.assertEqual(task.assigned_to.username, "testuser")

    def test_update_task_serializer(self):
        task = Task.objects.create(**self.task_data)
        updated_data = {
            "id": task.id,
            "name": "Updated Task",
            "description": "Updated Task Description",
            "due_date": timezone.now(),
            "status": "In Progress"
        }
        serializer = CreateOrUpdateTaskSerializer(instance=task, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_task = serializer.save()
        self.assertEqual(updated_task.name, "Updated Task")
        self.assertEqual(updated_task.status, "In Progress")

    def test_invalid_task_serializer(self):
        invalid_data = {
            "description": "Test Task Description",
            "due_date": timezone.now(),
            "status": "Pending"
        }
        serializer = CreateOrUpdateTaskSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_delete_task_serializer(self):
        task = Task.objects.create(**self.task_data)
        delete_data = {
            "id": task.id
        }
        serializer = DeleteTasksApiRequestSerializer(data=delete_data)
        self.assertTrue(serializer.is_valid())

        # Now delete the task using its ID
        task.delete()

        # Optionally, assert that the task has been deleted from the database
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task.id)
