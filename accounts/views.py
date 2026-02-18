from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer

from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token


# Create your views here.

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    # This allows anyone to access this view without a token
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. Get credentials from the Postman request
        username = request.data.get('username')
        password = request.data.get('password')

        # 2. Authenticate the user against the database
        user = authenticate(username=username, password=password)

        if user is not None:
            # 3. Get or Create a Token for the user
            token, created = Token.objects.get_or_create(user=user)

            # 4. Return the Token along with user info
            return Response({
                "message": "Login successful!",
                "token": token.key,  # The "key" they will use in Postman headers
                "user": user.username,
                "role": user.role
            }, status=status.HTTP_200_OK)
        else:
            # 5. Return an error message if credentials fail
            return Response({
                "error": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)

# This view only allows GET requests to see all users
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()           # Fetch all users from the DB
    serializer_class = UserSerializer       # Use the translator we built earlier