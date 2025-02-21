from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginTests(APITestCase):
    """Test cases for user login"""

    def setUp(self):
        self.login_url = "/api/auth/login"
        self.user = User.objects.create_user(email="test@example.com", password="Test@1234")

    def test_login_valid_user(self):
        """Test successful login"""
        data = {"email": "test@example.com", "password": "Test@1234"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data) 

    def test_login_invalid_password(self):
        """Test login with incorrect password"""
        data = {"email": "test@example.com", "password": "WrongPass"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_email(self):
        """Test login with incorrect password"""
        data = {"email": "test2@example.com", "password": "Test@1234"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
