# tasks/tests/test_views.py
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from tasks.views import TaskListingApiView, DeleteTasksApiView, AssignTasksApiView, CreateOrUpdateTasksApiView
from tasks.models import Task
from tasks.serializers import CreateOrUpdateTaskSerializer, DeleteTasksApiRequestSerializer, AssignTasksSerializer
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import json
from projects.models import Project
from users.models import User
from datetime import datetime, timedelta
from django.utils import timezone

class TaskViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', role='manager')
        self.project = Project.objects.create(name="Test Project")
        
        # Get token and authenticate
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_or_update_task_view(self):
        url = '/tasks/create-or-update-tasks/'
        due_date = timezone.now() + timedelta(days=7)
        data = {
            "project": self.project.id,
            "name": "New Task",
            "description": "Task Description",
            "assigned_to": self.user.id,
            "due_date": due_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "status": "Pending"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(">>>>>>>>create or update<<<<<<<<<<<<<<<<",response.data)
        
    def test_task_listing_view(self):
        url = '/tasks/listing-of-tasks/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task_view(self):
        task = Task.objects.create(
            project=self.project,
            name='Test Task',
            description='Test Description',
            assigned_to=self.user,
            due_date=timezone.now() + timedelta(days=7),
            status='Pending'
        )
        url = '/tasks/delete-tasks/'
        data = {'id': task.id}
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assign_task_view(self):
        task = Task.objects.create(
            project=self.project,
            name='Test Task',
            description='Test Description',
            due_date=timezone.now() + timedelta(days=7),
            status='Pending'
        )
        url = '/tasks/assign-tasks/'
        data = {'id': task.id, 'assigned_to': self.user.id}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
