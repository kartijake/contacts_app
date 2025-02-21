from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from core.utils.error_formatter import format_serializer_errors
class RegisterUserView(APIView):
    """API endpoint for user registration"""
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if not serializer.is_valid():
             return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            

        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class LoginUserView(APIView):
    """API endpoint for user login"""
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)