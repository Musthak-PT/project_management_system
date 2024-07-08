from django.test import TestCase
from milestones.models import Milestone
from projects.models import Project
from django.utils import timezone

class MilestoneModelTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.milestone = Milestone.objects.create(
            project=self.project,
            name="Test Milestone",
            due_date=timezone.now()
        )

    def test_milestone_creation(self):
        self.assertEqual(self.milestone.name, "Test Milestone")
        self.assertEqual(self.milestone.project, self.project)