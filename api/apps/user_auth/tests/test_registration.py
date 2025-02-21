from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTests(APITestCase):
    """Test cases for user registration"""

    def setUp(self):
        """Set up test environment"""
        self.register_url = "/api/auth/register"
        self.user = User.objects.create_user(email="existing@example.com", password="Existing@1234")

    def test_register_new_user(self):
        """Test successful registration of a new user"""
        data = {"email": "newuser@example.com", "password": "NewPass@123"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User registered successfully")

    def test_register_existing_user(self):
        """Test registering an existing user (should fail)"""
        data = {"email": "existing@example.com", "password": "NewPass@123"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('email, user with this email already exists.', response.data["message"])

    def test_register_with_weak_password(self):
        """Test registration with a weak password (should fail)"""
        data = {"email": "userweak@example.com", "password": "weakpass"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("password, must contain at least one uppercase letter.", response.data["message"])

    def test_register_with_missing_fields(self):
        """Test registration with missing email or password (should fail)"""
        data = {"email": "user@example.com"}  # Missing password
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('password, this field is required.', response.data["message"])

    def test_register_with_invalid_email(self):
        """Test registration with an invalid email format (should fail)"""
        data = {"email": "invalidemail", "password": "Valid@123"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("email, enter a valid email address.", response.data["message"])

    def test_register_with_strong_password(self):
        """Test registration with a strong password (should pass)"""
        data = {"email": "strongpass@example.com", "password": "StrongPass@123"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User registered successfully")
