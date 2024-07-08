from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tasks.models import Task
from projects.models import Project
from users.models import User
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

class TaskViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', role='manager')
        self.project = Project.objects.create(name="Test Project",description='Test Project',members=self.user)
        self.task = Task.objects.create(
            project=self.project,
            name="Test Task",
            description="Test Task Description",
            assigned_to=self.user,
            due_date=timezone.now(),
            status="Pending"
        )
        # self.client.force_login(self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_task_listing_view(self):
        url = reverse('tasks:listing-task')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task_view(self):
        url = reverse('tasks:create-or-update-tasks')
        data = {
            "project": self.project.id,
            "name": "New Task",
            "description": "New Task Description",
            "assigned_to": self.user.id,
            "due_date": timezone.now(),
            "status": "Pending"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(">>>>>>>>>>>>>>>Creation>>>>>>>>>>>", response.data)

    def test_update_task_view(self):
        url = reverse('tasks:create-or-update-tasks')
        data = {
            "id": self.task.id,
            "name": "Updated Task Name",
            "description": "Updated Task Description",
            "due_date": timezone.now(),
            "status": "In Progress"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(">>>>>>>>>>>>>>>Updation>>>>>>>>>>>", response.data)
        
    def test_delete_task_view(self):
        url = reverse('tasks:delete-tasks')
        data = {
            "id": self.task.id
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(">>>>>>>>>>>>>>>Deletion>>>>>>>>>>>", response.data)
        
    def test_assign_task_view(self):
        url = reverse('tasks:assign-tasks')
        data = {
            "id": self.task.id,
            "assigned_to": self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
