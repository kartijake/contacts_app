from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.contacts.models import Contact, Telephone

User = get_user_model()

class GetContactsTests(APITestCase):
    """Test cases for retrieving contacts via GET request"""

    def setUp(self):
        """Set up test data"""
        # Creating a user and authenticate them
        self.user = User.objects.create_user(email="test@example.com", password="Test@1234")
        self.client.force_authenticate(user=self.user)

        # Creating multiple contacts for the user
        self.contact1 = Contact.objects.create(user=self.user, name="John Doe", address_line_1="123 Street")
        self.contact2 = Contact.objects.create(user=self.user, name="Jane Doe", address_line_1="456 Avenue")
        self.contact3 = Contact.objects.create(user=self.user, name="Alice Johnson", address_line_1="789 Blvd")

        # Add telephone numbers for the contacts
        Telephone.objects.create(user=self.user,contact=self.contact1, number="+123456789")
        Telephone.objects.create(user=self.user,contact=self.contact2, number="+987654321")
        Telephone.objects.create(user=self.user,contact=self.contact3, number="+112233445")

        self.contacts_url = "/api/contacts"

    def test_get_contacts_success(self):
        """Test retrieving all contacts (authenticated user)"""
        response = self.client.get(self.contacts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]),3) 
        self.assertIn("name", response.data["results"][0])  
        self.assertIn("telephones", response.data["results"][0])  

    def test_get_contacts_unauthenticated(self):
        """Test retrieving contacts without authentication (should fail)"""
        self.client.logout()
        response = self.client.get(self.contacts_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_pagination_details_in_response(self):
        """Test pagination details are included in the response"""
        response = self.client.get(self.contacts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)  
        self.assertIn("next", response.data) 
        self.assertIn("previous", response.data)  
    
    def test_search_contacts_by_substring(self):
        """Test searching contacts using a substring query (?q=)"""
        response = self.client.get(f"{self.contacts_url}/search?q=John")  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)
        results = [contact["name"] for contact in response.data["results"]]
        self.assertIn("John Doe", results)
        self.assertIn("Alice Johnson", results)
        self.assertNotIn("Jane Doe", results) 
    
    def test_search_no_results(self):
        """Test search with a non-matching query (should return empty results)"""
        response = self.client.get(f"{self.contacts_url}/search?q=XYZ")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0) 

    def test_pagination_in_search_results(self):
        """Test that search results still include pagination details"""
        response = self.client.get(f"{self.contacts_url}/search?q=John")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)  
        self.assertIn("next", response.data)  
        self.assertIn("previous", response.data)  