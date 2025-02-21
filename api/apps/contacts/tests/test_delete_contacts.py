from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.contacts.models import Contact, Telephone

User = get_user_model()

class DeleteContactTests(APITestCase):
    """Test cases for deleting contacts via DELETE request"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(email="test@example.com", password="Test@1234")
        self.client.force_authenticate(user=self.user)  # Authenticate user

        self.contact = Contact.objects.create(user=self.user, name="John Doe", address_line_1="123 Street")
        self.contact_url = f"/api/contacts/{self.contact.id}"

        self.phone = Telephone.objects.create(user=self.user,contact=self.contact, number="+123456789")

        self.other_user = User.objects.create_user(email="other@example.com", password="Test@1234")
        self.other_contact = Contact.objects.create(user=self.other_user, name="Jane Doe")
        self.other_contact_url = f"/api/contacts/{self.other_contact.id}"

    def test_delete_contact_success(self):
        """Test successfully deleting a contact"""
        response = self.client.delete(self.contact_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())

    def test_delete_contact_also_deletes_telephones(self):
        """Test that deleting a contact also deletes associated telephone numbers"""
        response = self.client.delete(self.contact_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Telephone.objects.filter(contact=self.contact).exists())

    def test_delete_non_existent_contact_fail(self):
        """Test deleting a contact that does not exist"""
        invalid_contact_url = "/api/contacts/9999/"  
        response = self.client.delete(invalid_contact_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_contact_unauthenticated_fail(self):
        """Test deleting a contact without authentication"""
        self.client.logout()  # Unauthenticate user
        response = self.client.delete(self.contact_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_delete_other_users_contact_fail(self):
        """Test attempting to delete another user's contact"""
        response = self.client.delete(self.other_contact_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
        self.assertEqual(response.data["message"], "Contact not found or you do not have permission to delete it.") 
