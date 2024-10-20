# tasks/tests/test_api.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Task  # Adjust the import based on your Task model's location

class TaskManagementAPITests(APITestCase):
    
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        
        # Create a token for the user
        self.token = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'password123'
        }).data['access']

    def test_create_task(self):
        """Test creating a task"""
        url = reverse('task-list')  # Adjust to your task list endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, {
            'title': 'New Task',
            'description': 'Task description',
            'due_date': '2024-10-30T12:00:00Z',
            'priority': 'medium',
            'status': 'pending'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'New Task')

    def test_list_tasks(self):
        """Test listing tasks"""
        Task.objects.create(
            title='Test Task 1',
            description='Description 1',
            due_date='2024-10-30T12:00:00Z',
            priority='low',
            status='pending',
            user=self.user  # If you have user ownership for tasks
        )
        url = reverse('task-list')  # Adjust to your task list endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_task(self):
        """Test retrieving a specific task"""
        task = Task.objects.create(
            title='Retrieve Task',
            description='Retrieve this task',
            due_date='2024-10-30T12:00:00Z',
            priority='high',
            status='pending',
            user=self.user  # If applicable
        )
        url = reverse('task-detail', args=[task.id])  # Adjust to your task detail endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], task.title)

    def test_update_task(self):
        """Test updating a task"""
        task = Task.objects.create(
            title='Update Task',
            description='Original description',
            due_date='2024-10-30T12:00:00Z',
            priority='medium',
            status='pending',
            user=self.user  # If applicable
        )
        url = reverse('task-detail', args=[task.id])  # Adjust to your task detail endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(url, {
            'title': 'Updated Task',
            'description': 'Updated description',
            'due_date': '2024-11-01T12:00:00Z',
            'priority': 'high',
            'status': 'completed'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')

    def test_delete_task(self):
        """Test deleting a task"""
        task = Task.objects.create(
            title='Delete Task',
            description='This task will be deleted',
            due_date='2024-10-30T12:00:00Z',
            priority='low',
            status='pending',
            user=self.user  # If applicable
        )
        url = reverse('task-detail', args=[task.id])  # Adjust to your task detail endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

