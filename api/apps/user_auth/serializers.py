from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.utils.password_validator import CustomPasswordValidator
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate_password(self, value):
        """Apply the custom password policy"""
        validator = CustomPasswordValidator()
        validator.validate(value)
        return value

    def create(self, validated_data):
        """Create a new user with an encrypted password"""
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate user and return JWT tokens"""
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError({"message": "Invalid email or password"})

        refresh = RefreshToken.for_user(user)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "email":user.email
        }


    """API endpoint to search contacts by name or telephone number"""
    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response({"message": "Search query is required."}, status=status.HTTP_400_BAD_REQUEST)

        contacts = Contact.objects.filter(
            Q(name__icontains=query) | Q(telephones__number__icontains=query),
            user=request.user
        ).distinct()

        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)