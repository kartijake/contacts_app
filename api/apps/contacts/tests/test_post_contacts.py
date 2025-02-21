from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.contacts.models import Contact, Telephone

User = get_user_model()

class CreateContactTests(APITestCase):
    """Test cases for creating contacts via POST request"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(email="test@example.com", password="Test@1234")
        self.client.force_authenticate(user=self.user)  

        # API URL
        self.create_url = "/api/contacts"

    def test_create_contact_success(self):
        """Test successfully creating a contact"""
        data = {
            "name": "John Doe",
            "address_line_1": "123 Main St",
            "address_line_2": "Main St",
            "city": "New York",
            "country": "USA",
            "postcode":"123 123",
            "telephones": [{"number": "+123456789"}]
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Contact created successfully")
        self.assertTrue(Contact.objects.filter(name="John Doe").exists())
        self.assertTrue(Telephone.objects.filter(number="+123456789").exists())

    def test_create_contact_with_multiple_phones(self):
        """Test creating a contact with multiple phone numbers"""
        data = {
            "name": "Alice Johnson",
            "address_line_1": "456 Elm St",
            "city": "Los Angeles",
            "country": "USA",
            "telephones": [
                {"number": "+111111111"},
                {"number": "+222222222"}
            ]
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Telephone.objects.filter(contact__name="Alice Johnson").count(), 2)

    def test_create_contact_missing_fields(self):
        """Test creating a contact with missing required fields"""
        data = {
            "address_line_1": "789 Broadway St"  
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data["message"])  

    def test_create_contact_unauthenticated(self):
        """Test creating a contact without authentication"""
        self.client.logout()  
        data = {
            "name": "Unauthenticated User",
            "telephones": [{"number": "+333333333"}]
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_create_contact_duplicate_phone_number_for_same_user(self):
        """Test preventing duplicate phone numbers for the same user"""
        data = {
            "name": "Duplicate Phone",
            "telephones": [{"number": "+123456789"}]  
        }
        self.client.post(self.create_url, data, format="json")
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("telephones", response.data["message"]) 