# tests/test_serializers.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from projects.models import Project
from projects.serializers import CreateOrUpdateProjectSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class ProjectSerializerTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', role='manager')
        self.project_data = {
            'name': 'Test Project',
            'description': 'This is a test project description'
        }
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_valid_serializer(self):
        serializer = CreateOrUpdateProjectSerializer(data=self.project_data)
        self.assertTrue(serializer.is_valid())

    def test_create_project(self):
        serializer = CreateOrUpdateProjectSerializer(data=self.project_data)
        self.assertTrue(serializer.is_valid())  # Ensure data is valid before saving
        if serializer.is_valid():
            project_instance = serializer.save()
            self.assertEqual(project_instance.name, 'Test Project')
