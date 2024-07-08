# projects/tests/test_serializers.py

from django.test import TestCase
from projects.models import Project
from users.models import User
from projects.serializers import CreateOrUpdateProjectSerializer, DeleteProjectApiRequestSerializer

class ProjectSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.project_data = {
            "name": "Test Project",
            "description": "Test Description",
            "members": [self.user.id]  # Use IDs for members
        }
        self.project = Project.objects.create(name="Test Project", description="Test Description")
        self.project.members.set([self.user])  # Assign members correctly

    def test_valid_project_serializer(self):
        serializer = CreateOrUpdateProjectSerializer(data=self.project_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_project_serializer(self):
        invalid_data = {  # Ensure this data is truly invalid
            "description": "Test Description",  # Missing 'name' or other required fields
        }
        serializer = CreateOrUpdateProjectSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
