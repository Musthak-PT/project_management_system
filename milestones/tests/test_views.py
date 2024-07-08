from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from milestones.models import Milestone
from projects.models import Project
from django.utils import timezone
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

class MilestoneViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', role='admin')
        self.project = Project.objects.create(name="Test Project")
        self.milestone = Milestone.objects.create(project=self.project, name="Test Milestone",
                                                  due_date=timezone.now().date())

        # Get token and authenticate
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_milestones(self):
        url = reverse('milestones:listing-milestone')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_milestone(self):
        url = reverse('milestones:create-or-update-milestone')
        due_date = datetime.now().date() + timezone.timedelta(days=7)  # Example due date
        data = {
            "project": self.project.id,
            "name": "New Milestone",
            "due_date": due_date.strftime('%Y-%m-%d')  # Format due_date properly
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(">>>>>>>>>>>>>>Milestone creation>>>>>>>>>>>>>>", response.data)
        milestone_id = response.data['data']['id']

        # Test milestone update
        updated_data = {
            "id": milestone_id,
            "project": self.project.id,
            "name": "Updated Milestone",
            "due_date": due_date.strftime('%Y-%m-%d')
        }
        update_url = reverse('milestones:create-or-update-milestone')
        update_response = self.client.post(update_url, updated_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_201_CREATED)
        print(">>>>>>>>>>>>>>Milestone update>>>>>>>>>>>>>>", update_response.data)

        # Test milestone deletion
        delete_url = reverse('milestones:delete-milestone')
        delete_data = {'id': milestone_id}
        delete_response = self.client.delete(delete_url, delete_data, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        print(">>>>>>>>>>>>>>Milestone deletion>>>>>>>>>>>>>>", delete_response.data)
