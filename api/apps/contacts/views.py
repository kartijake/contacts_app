from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Contact
from .serializers import ContactSerializer
from core.utils.error_formatter import format_serializer_errors
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
class ContactPagination(PageNumberPagination):
    """Custom pagination for contacts"""
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50

@extend_schema(tags=["Contacts"])
class ContactListView(APIView):
    """Handles listing, creating """
    permission_classes = [IsAuthenticated]  # Require authentication
    @extend_schema(
        summary="List Contacts",
        description="Retrieve all contacts of the authenticated user with pagination.",
        parameters=[
            OpenApiParameter(name="page", description="Page number", required=False, type=int),
            OpenApiParameter(name="page_size", description="Number of items per page", required=False, type=int),
        ],
        responses={200: OpenApiResponse(
            description="Successful request",
            response=ContactSerializer(many=True),
            examples=[OpenApiExample(
                name="Successful Contact Update",
                value={
                    "count": 30,
                    "next": "/api/contacts?page=2",
                    "previous": "null",
                    "results": [{
                            "id": 1,
                            "name": "John Doe",
                            "address_line_1": "123 Street",
                            "city": "New York",
                            "country": "USA",
                            "postcode": "10001",
                            "telephones": [{"number": "+123456789"}]
                        }]},
                    response_only=True,
            ),]
        )},
    )
    def get(self, request):
        """List all contacts for the authenticated user with pagination"""
        contacts = Contact.objects.filter(user=request.user).order_by("-created_at")

        paginator = ContactPagination()
        result_page = paginator.paginate_queryset(contacts, request)
        serializer = ContactSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create Contact",
        description="Create a new contact for the authenticated user.",
        request=ContactSerializer,
        responses={
            201:OpenApiResponse(
            response=ContactSerializer,
            description="Contact created successfully",
            examples=[
                OpenApiExample(
                    name="Successful Contact Creation",
                    value={
                        "message": "Contact created successfully",
                        "contact": {
                            "id": 1,
                            "name": "John Doe",
                            "address_line_1": "123 Street",
                            "city": "New York",
                            "country": "USA",
                            "postcode": "10001",
                            "telephones": [{"number": "+123456789"}]
                        }
                    },
                    response_only=True,
                )
            ]),
            400: OpenApiResponse(
            description="Validation Error",
            response=({"message": "`Filed`, this field is required."}),
            examples=[
                OpenApiExample(
                    name="Validation Error (Missing Name)",
                    description="Missing required field: `name`",
                    value={"message": "name, this field is required."},
                    response_only=True,
                ),
                    OpenApiExample(
                    name="Validation Error (Missing Telephone number)",
                    description="Missing required field: `telephones`",
                    value={"message": "telephones, this field is required."},
                    response_only=True,
                )
                ]
        )
        }
    )

    def post(self, request):
        """Create a new contact for the authenticated user"""
        serializer = ContactSerializer(data=request.data, context={"request": request})

        if not serializer.is_valid():
            return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Contact created successfully", "contact": serializer.data}, status=status.HTTP_201_CREATED)
    
    
@extend_schema(tags=["Contacts"])
class ContactDetailView(APIView):
    """Handles Update and Delete """
    @extend_schema(
        summary="Update Contact",
        description="Partially update an existing contact if it belongs to the authenticated user.",
        request=ContactSerializer,
        responses={
            200: OpenApiResponse(
                response=ContactSerializer,
                description="Successful Contact Update",
                examples=[OpenApiExample(
                name="Successful Contact Update",
                value={"message": "Contact updated successfully", "contact":  {
                            "id": 1,
                            "name": "John Doe",
                            "address_line_1": "123 Street",
                            "city": "New York",
                            "country": "USA",
                            "postcode": "10001",
                            "telephones": [{"number": "+123456789"}]
                        }},
                response_only=True,
            ),]
            ),            
            404: OpenApiResponse(
                description="Contact Not Found",
                response={"message": "Contact not found or you do not have permission to update it."},
                examples=[OpenApiExample(
                name="Contact Not Found",
                value={"message": "Contact not found or you do not have permission to update it."},
                response_only=True,
            )
                ]
            )
        },
    )
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
    
    @extend_schema(
        summary="Delete Contact",
        description="Delete a contact if it belongs to the authenticated user.",
        responses={
            204:OpenApiResponse(
                description="Successful Contact Deletion",
                response={"message": "Contact deleted successfully"},
                examples=[OpenApiExample(
                name="Successful Contact Deletion",
                value={"message": "Contact deleted successfully"},
                response_only=True,
            ),
                ]
            ),
            404: OpenApiResponse(
                description="Contact Not Found",
                response={"message": "Contact not found or you do not have permission to delete it."},
                examples=[
                    OpenApiExample(
                name="Contact Not Found",
                value={"message": "Contact not found or you do not have permission to delete it."},
                response_only=True,
            ),
                ]
            )
        },
    )
    def delete(self, request, contact_id):
        """Delete a contact if it belongs to the authenticated user"""
        try:
            contact = Contact.objects.get(id=contact_id, user=request.user)
        except Contact.DoesNotExist:
            return Response({"message": "Contact not found or you do not have permission to delete it."}, status=status.HTTP_404_NOT_FOUND)

        contact.delete()
        return Response({"message": "Contact deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=["Contacts"])
class SearchContactsView(APIView):
    """API endpoint to search contacts by name or telephone number"""
    pagination_class = ContactPagination()

    @extend_schema(
        summary="Search Contacts",
        description="Search contacts by name or telephone number.",
        parameters=[
            OpenApiParameter(name="q", description="Search query (name or phone number)", required=True, type=str),
        ],
        responses={
            200: OpenApiResponse(
                response=ContactSerializer(),
                description="List of matching contacts",
                examples=[OpenApiExample(
                name="Successful Contact Update",
                value={
                    "count": 30,
                    "next": "/api/contacts?page=2",
                    "previous": "null",
                    "results": [{
                            "id": 1,
                            "name": "John Doe",
                            "address_line_1": "123 Street",
                            "city": "New York",
                            "country": "USA",
                            "postcode": "10001",
                            "telephones": [{"number": "+123456789"}]
                        }]},
                    response_only=True,
            ),]
            ),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        name="Missing Query Parameter",
                        description="Search query `q` is required",
                        value={"message": "Search query is required."},
                        response_only=True,
                    )
                ],
            ),
        },
    )
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

        return paginator.get_paginated_response(serializer.data)