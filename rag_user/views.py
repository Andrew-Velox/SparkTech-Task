# from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from .serializers import (
    RegistrationSerializer,
    UserLoginSerializer,
)
from .tasks import send_verification_email_task

# User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Sign-up a new user",
        # description="""
        # signup a new user account with email verification.
        
        # **Process:**
        # 1. User submits registration data.
        # 2. System validates data and creates user account.
        
        # **Required Fields:**
        # - username
        # - email
        # - password
        # - confirm_password
        
        # **Response:**
        # - Success: Registration successful. Please check your email.
        # - Error: Validation errors with field-specific messages
        
        # **Examples:**
        
        # ```json
        # {
        #     "username": "string",
        #     "email": "user@example.com",
        #     "password": "string",
        #     "confirm_password": "string"
        # }
        # ```

        # """,
        request=RegistrationSerializer,
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        }
    )

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Send verification email in background
            send_verification_email_task(user.email, user.username)
            
            return Response(
                {"detail": "Registration successful. Please check your email."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="User Login",
        # description="""
        # Authenticate a user and retrieve JWT tokens.
        
        # **Process:**
        # 1. User submits login credentials (username/email and password).
        # 2. System validates credentials and returns JWT tokens.
        
        # **Required Fields:**
        # - username_or_email
        # - password
        
        # **Response:**
        # - Success: Returns access token, refresh token, and user info
        # - Error: Validation errors or invalid credentials message
        
        # **Example Request:**
        # ```json
        # {
        #     "username_or_email": "johndoe",
        #     "password": "SecurePass123"
        # }
        # ```
        
        # **Example Success Response:**
        # ```json
        # {
        #     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci...",
        #     "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
        #     "user": {
        #         "id": 1,
        #         "username": "johndoe",
        #         "email": "john@example.com"
        #     }
        # }
        # ```
        
        # **Common Errors:**
        # - Invalid username/email or password
        # - User account is not active
        # """,
        request=UserLoginSerializer,
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)