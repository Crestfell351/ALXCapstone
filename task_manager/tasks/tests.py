from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task


class TaskManagementAPITests(APITestCase):

    def setUp(self):
        """
        Set up initial data, including creating a user and logging in to obtain an auth token
        """
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        # URL endpoints
        self.tasks_url = reverse('task-list')  # e.g., /api/tasks/
        self.create_task_url = reverse('task-list')
    
    def test_create_task(self):
        """
        Test that a user can create a task
        """
        task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "due_date": "2024-10-20",
            "priority": "High",
            "status": "Pending"
        }

        response = self.client.post(self.create_task_url, task_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test Task")
    
    def test_get_all_tasks(self):
        """
        Test that a user can retrieve all their tasks
        """
        Task.objects.create(title="Task 1", description="First task", due_date="2024-10-21", priority="Medium", status="Pending", user=self.user)
        Task.objects.create(title="Task 2", description="Second task", due_date="2024-10-22", priority="High", status="Pending", user=self.user)

        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_task_by_id(self):
        """
        Test retrieving a single task by its ID
        """
        task = Task.objects.create(title="Task Detail", description="Task detail test", due_date="2024-10-23", priority="Low", status="Pending", user=self.user)

        task_url = reverse('task-detail', kwargs={"pk": task.id})  # e.g., /api/tasks/1/
        response = self.client.get(task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Task Detail")
    
    def test_update_task(self):
        """
        Test updating a task
        """
        task = Task.objects.create(title="Update Task", description="Update task description", due_date="2024-10-25", priority="Low", status="Pending", user=self.user)
        task_url = reverse('task-detail', kwargs={"pk": task.id})  # e.g., /api/tasks/1/

        updated_data = {
            "title": "Updated Task",
            "description": "Updated description",
            "due_date": "2024-10-26",
            "priority": "High",
            "status": "Pending"
        }

        response = self.client.put(task_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Task")
    
    def test_delete_task(self):
        """
        Test deleting a task
        """
        task = Task.objects.create(title="Delete Task", description="Delete task test", due_date="2024-10-27", priority="Low", status="Pending", user=self.user)
        task_url = reverse('task-detail', kwargs={"pk": task.id})  # e.g., /api/tasks/1/

        response = self.client.delete(task_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_mark_task_as_complete(self):
        """
        Test marking a task as complete
        """
        task = Task.objects.create(title="Complete Task", description="Complete task description", due_date="2024-10-28", priority="Medium", status="Pending", user=self.user)
        complete_url = reverse('task-complete', kwargs={"pk": task.id})  # e.g., /api/tasks/1/complete/

        response = self.client.patch(complete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Completed")
    
    def test_filter_tasks(self):
        """
        Test filtering tasks by status and priority
        """
        Task.objects.create(title="Task 1", description="Task 1 description", due_date="2024-10-30", priority="High", status="Completed", user=self.user)
        Task.objects.create(title="Task 2", description="Task 2 description", due_date="2024-10-31", priority="Medium", status="Pending", user=self.user)

        # Filtering by status
        response = self.client.get(f"{self.tasks_url}?status=Pending")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Filtering by priority
        response = self.client.get(f"{self.tasks_url}?priority=High")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

