# tests/test_views.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from projects.models import Project
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class ProjectViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', role='manager')
        self.project = Project.objects.create(name="Test Project")
        self.project_url = reverse('projects:listing-project')

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_project_listing(self):
        response = self.client.get(self.project_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project(self):
        new_project_data = {
            'name': 'New Project',
            'description': 'This is a new project'
        }
        response = self.client.post(reverse('projects:create-or-update-project'), new_project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(">>>>>>Creation>>>>>>>",response.data)
