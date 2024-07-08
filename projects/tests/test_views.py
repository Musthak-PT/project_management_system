# projects/tests/test_views.py

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from projects.models import Project
from users.models import User
from projects.serializers import CreateOrUpdateProjectSerializer, DeleteProjectApiRequestSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class ProjectViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', role='manager')
        self.admin = User.objects.create_user(username='adminuser', password='adminpass', role='admin')
        self.member = User.objects.create_user(username='memberuser', password='memberpass', role='member')
        self.project = Project.objects.create(name="Test Project", description="Test Description")
        self.project.members.add(self.user.id)  # Assign member to project
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_project_listing(self):
        url = reverse('projects:listing-project')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project(self):
        url = reverse('projects:create-or-update-project')
        data = {
            "name": "New Project",
            "description": "New Project Description"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(">>>>>>>>>>>>>>>Creation>>>>>>>>>>", response.data)

    def test_update_project(self):
        url = reverse('projects:create-or-update-project')
        data = {
            'name': 'Updated Project Name',
            'description': 'Updated Project Description',
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Correct expected status code

    def test_delete_project(self):
        url = reverse('projects:delete-project')  # Fix the reverse function call
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Correct expected status code

    def test_invalid_project_serializer(self):
        url = reverse('projects:create-or-update-project')
        invalid_data = {  # Missing 'name'
            "description": "Test Description"
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
