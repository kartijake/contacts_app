from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from core.utils.error_formatter import format_serializer_errors
from rest_framework_simplejwt.views import TokenRefreshView


@extend_schema(tags=["Auth"])

class RegisterUserView(APIView):
    """API endpoint for user registration"""
    permission_classes = [permissions.AllowAny]
    @extend_schema(
    summary="Register user",
    description="Allows users to create an account with an email and password.",
    request=UserRegistrationSerializer,
    responses={200: {"message": "User registered successfully"}, 400: { "message": "email, user with this email already exists."}},
    examples=[
         OpenApiExample(
            name="Successful Response",
            description="Example of a successful response",
            value={"message": "User registered successfully"},
            response_only=True
        ), 
        OpenApiExample(
            name="Duplicate email",
            description="Example of a email already existing",
            value={"message": "email, user with this email already exists."},
            response_only=True,
            status_codes=[400] 
        ),
        OpenApiExample(
            name="Weak password",
            description="Example of a weak password",
            value={"message": "password, must be at least 8 characters long."},
            response_only=True,
            status_codes=[400] 
        ),
    ]
)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if not serializer.is_valid():
             return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            

        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

@extend_schema(tags=["Auth"])

class LoginUserView(APIView):
    """API endpoint for user login"""
    permission_classes = [permissions.AllowAny]
    @extend_schema(
    summary="User Login",
    description="Allows users to log in with their email and password to obtain access and refresh tokens.",
    request=UserLoginSerializer,
    responses={200: {"access_token": "JWT access token", "refresh_token": "JWT refresh token", "email":"Users registered email"}, 400: {"message": "Invalid email or password"}},
    examples=[
        OpenApiExample(
            name="Successful Response",
            description="Example of a successful response with JWT tokens",
            value={
                "access_token": "jwt_access_token",
                "refresh_token": "jwt_refresh_token",
                "email":"registered_email"
            },
            response_only=True
        ), 
        OpenApiExample(
            name="Failed Login",
            description="Example of a failed login attempt due to invalid credentials",
            value={"message": "Invalid email or password"},
            response_only=True,
            status_codes=[400] 
        ),
    ]
)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Refresh Access Token",
    description="""
        This endpoint allows users to refresh their JWT access token using a valid refresh token.
        If the refresh token is expired or invalid, the request will be denied.
    """,
    request={
        "application/json": {
            "refresh": "string (JWT refresh token)"
        }
    },
    responses={
        200: {"access": "string (New JWT access token)"},
        401: {
            "detail": "Token is invalid or expired",
            "code": "token_not_valid"
        }
    },
    examples=[
        OpenApiExample(
            name="Valid Refresh Token",
            description="Example of a successful token refresh request",
            value={"refresh": "your_valid_refresh_token_here"},
            request_only=True,
        ),
        OpenApiExample(
            name="Successful Refresh Token",
            description="Example of a successful token refresh",
            value={"access": "new_JWT_access_token"},
            request_only=False,
        ),
        OpenApiExample(
            name="Invalid Refresh Token",
            description="Example of a failed token refresh request due to an invalid token",
            value={"detail": "Token is invalid or expired", "code": "token_not_valid"},
            response_only=True,
            status_codes=[401] 
        ),
    ]
) 
@extend_schema(tags=["Auth"])

class CustomTokenRefreshView(TokenRefreshView):
    """Customized Token Refresh View for documentation"""
    pass