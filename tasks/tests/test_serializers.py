# tasks/tests/test_serializers.py
from django.test import TestCase
from tasks.models import Task
from tasks.serializers import CreateOrUpdateTaskSerializer

class TaskSerializerTest(TestCase):
    def setUp(self):
        self.task_data = {
            'project': 1,  # Assuming project ID exists in your database
            'name': 'Test Task',
            'description': 'Test Description',
            'assigned_to': 1,  # Assuming user ID exists in your database
            'due_date': '2024-07-08T12:00:00Z',
            'status': 'Pending'
        }
    
    def test_task_serializer_valid(self):
        serializer = CreateOrUpdateTaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())
        
    def test_task_serializer_invalid(self):
        invalid_data = self.task_data.copy()
        invalid_data['due_date'] = 'invalid_date_format'
        serializer = CreateOrUpdateTaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
