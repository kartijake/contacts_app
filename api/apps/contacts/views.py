from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Contact
from .serializers import ContactSerializer
from core.utils.error_formatter import format_serializer_errors
from django.db.models import Q
class ContactPagination(PageNumberPagination):
    """Custom pagination for contacts"""
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50

class ContactView(APIView):
    """Handles listing and creating contacts"""

    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        """List all contacts for the authenticated user with pagination"""
        contacts = Contact.objects.filter(user=request.user).order_by("-created_at")

        paginator = ContactPagination()
        result_page = paginator.paginate_queryset(contacts, request)
        serializer = ContactSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Create a new contact for the authenticated user"""
        serializer = ContactSerializer(data=request.data, context={"request": request})

        if not serializer.is_valid():
            return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Contact created successfully", "contact": serializer.data}, status=status.HTTP_201_CREATED)
    
    def put(self, request, contact_id):
        """Partially update a contact if it belongs to the authenticated user"""
        try:
            contact = Contact.objects.get(id=contact_id, user=request.user)
        except Contact.DoesNotExist:
            return Response({"message": "Contact not found or you do not have permission to update it."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactSerializer(contact, data=request.data, partial=True, context={"request": request})

        if not serializer.is_valid():
            return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Contact updated successfully", "contact": serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request, contact_id):
        """Delete a contact if it belongs to the authenticated user"""
        try:
            contact = Contact.objects.get(id=contact_id, user=request.user)
        except Contact.DoesNotExist:
            return Response({"message": "Contact not found or you do not have permission to delete it."}, status=status.HTTP_404_NOT_FOUND)

        contact.delete()
        return Response({"message": "Contact deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class SearchContactsView(APIView):
    """API endpoint to search contacts by name or telephone number"""
    pagination_class = ContactPagination()
    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response({"message": "Search query is required."}, status=status.HTTP_400_BAD_REQUEST)

        contacts = Contact.objects.filter(
            Q(name__icontains=query) | Q(telephones__number__icontains=query),
            user=request.user
        ).distinct()
        paginator = self.pagination_class
        paginated_contacts = paginator.paginate_queryset(contacts, request)
        serializer = ContactSerializer(paginated_contacts, many=True)

        serializer = ContactSerializer(contacts, many=True)
        return paginator.get_paginated_response(serializer.data)