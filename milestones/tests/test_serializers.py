from django.test import TestCase
from milestones.models import Milestone
from milestones.serializers import CreateOrUpdateMilestoneSerializer
from projects.models import Project
from django.utils import timezone

class MilestoneSerializerTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.milestone_data = {
            "project": self.project.id,
            "name": "Test Milestone",
            "due_date": timezone.now().date()  # Ensure due_date matches serializer requirement
        }

    def test_valid_serializer(self):
        serializer = CreateOrUpdateMilestoneSerializer(data=self.milestone_data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)  # Include msg to show validation errors

    def test_invalid_serializer(self):
        invalid_data = self.milestone_data.copy()
        invalid_data['name'] = ""  # Assuming name is required
        serializer = CreateOrUpdateMilestoneSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())