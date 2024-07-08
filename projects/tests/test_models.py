# projects/tests/test_models.py

from django.test import TestCase
from projects.models import Project
from users.models import User

class ProjectModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.project_data = {
            "name": "Test Project",
            "description": "Test Description",
        }
        self.project = Project.objects.create(**self.project_data)
        self.project.members.set([self.user])  # Assign members correctly

    def test_project_creation(self):
        project = Project.objects.get(name="Test Project")
        self.assertEqual(project.description, "Test Description")

    def test_project_deletion(self):
        project = Project.objects.get(name="Test Project")
        project.delete()
        self.assertFalse(Project.objects.filter(name="Test Project").exists())
