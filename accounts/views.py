from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer

from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response


# Create your views here.

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        # 1. Get credentials from the Postman request
        username = request.data.get('username')
        password = request.data.get('password')

        # 2. Authenticate the user against the database
        user = authenticate(username=username, password=password)

        if user is not None:
            # 3. Return a clean JSON success message
            return Response({
                "message": "Login successful!",
                "user": user.username,
                "role": user.role
            }, status=status.HTTP_200_OK)
        else:
            # 4. Return an error message if credentials fail
            return Response({
                "error": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)

# This view only allows GET requests to see all users
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()           # Fetch all users from the DB
    serializer_class = UserSerializer       # Use the translator we built earlier