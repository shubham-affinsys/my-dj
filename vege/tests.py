from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Todo  # Adjust the import based on your project structure
from core.pagination import CustomPagination  # Adjust the import based on your project structure

class TodoAPITests(APITestCase):

    def setUp(self):
        # Create a user and some todos for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create some Todo objects
        self.todos = [
            Todo.objects.create(user=self.user, todo_title='Todo 1', todo_description='Description 1'),
            Todo.objects.create(user=self.user, todo_title='Todo 2', todo_description='Description 2'),
            Todo.objects.create(user=self.user, todo_title='Todo 3', todo_description='Description 3'),
        ]

    def tearDown(self):
        # Clean up after tests
        self.client.logout()

    def test_get_todos_success(self):
        # Arrange
        url = reverse('todo-list')  # Adjust the URL name based on your URL configuration

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 3)

    def test_get_todos_empty(self):
        # Arrange
        self.client.logout()  # Log out the user
        self.client.login(username='testuser', password='testpass')  # Log back in
        Todo.objects.all().delete()  # Delete all todos

        url = reverse('todo-list')  # Adjust the URL name based on your URL configuration

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

    def test_get_todos_unauthenticated(self):
        # Arrange
        self.client.logout()  # Ensure the user is logged out
        url = reverse('todo-list')  # Adjust the URL name based on your URL configuration

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Assuming you have permission checks

    def test_pagination(self):
        # Arrange
        url = reverse('todo-list')  # Adjust the URL name based on your URL configuration

        # Act
        response = self.client.get(url + '?page=1')  # Request the first page

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('links', response.data)
        self.assertIn('next', response.data['links'])
        self.assertIn('previous', response.data['links'])
        self.assertEqual(response.data['count'], 3)  # Total count of todos
        self.assertEqual(len(response.data['results']), 3)  # Number of results on the first page

