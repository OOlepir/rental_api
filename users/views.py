from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .cookies_manager import set_jwt_cookies
from .models import User
from .serializers import UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        password = request.data.get("password")
        email = request.data.get("email")
        user = authenticate(request, email=email, password=password)
        if user:
            response = Response(
                status=status.HTTP_200_OK, data={"message": "Logged in successfully"}
            )
            return set_jwt_cookies(response, user)
        return Response(
            status=status.HTTP_401_UNAUTHORIZED, data={"message": "Invalid credentials"}
        )

@api_view(["GET"])
def logout(request, *args, **kwargs):
    response = Response(
        status=status.HTTP_204_NO_CONTENT, data={"massage": "Successful logout"}
    )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
