# tests/test_models.py
from django.test import TestCase
from projects.models import Project
from users.models import User

class ProjectModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.project = Project.objects.create(
            name='Test Project',
            description='This is a test project description'
        )
        self.project.members.add(self.user)

    def test_project_creation(self):
        project = Project.objects.get(name='Test Project')
        self.assertEqual(project.description, 'This is a test project description')
        self.assertEqual(project.members.count(), 1)  # Check if user is added as a member
