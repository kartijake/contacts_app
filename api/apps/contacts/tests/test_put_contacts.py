from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.contacts.models import Contact, Telephone

User = get_user_model()

class UpdateContactTests(APITestCase):
    """Test cases for updating contacts via PUT request"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(email="test@example.com", password="Test@1234")
        self.client.force_authenticate(user=self.user) 
        self.contact = Contact.objects.create(user=self.user, name="John Doe", address_line_1="123 Street")
        self.contact_url = f"/api/contacts/{self.contact.id}"
        self.phone = Telephone.objects.create(user=self.user,contact=self.contact, number="+123456789")

    def test_update_contact_name_success(self):
        """Test successfully updating a contact's name"""
        data = {"name": "Updated Name"}
        response = self.client.put(self.contact_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_contact_with_new_phone_success(self):
        """Test updating a contact by adding a new phone number"""
        data = {"telephones": [{"number": "+987654321"}]} 
        response = self.client.put(self.contact_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Telephone.objects.filter(contact=self.contact, number="+987654321").exists())

    def test_update_contact_with_duplicate_phone_fail(self):
        """Test updating a contact with an already existing phone number"""
        another_contact = Contact.objects.create(user=self.user, name="Jane Doe")
        Telephone.objects.create(user=self.user,contact=another_contact, number="+555555555")

        data = {"telephones": [{"number": "+555555555"}]}  
        response = self.client.put(self.contact_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("telephones", response.data["message"])  

    def test_update_contact_unauthenticated_fail(self):
        """Test updating a contact without authentication"""
        self.client.logout()  
        data = {"name": "Unauthorized Update"}
        response = self.client.put(self.contact_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_update_non_existent_contact_fail(self):
        """Test updating a contact that does not exist"""
        invalid_contact_url = "/api/contacts/9999/"  
        data = {"name": "Non-existent Contact"}
        response = self.client.put(invalid_contact_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
