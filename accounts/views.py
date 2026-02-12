from rest_framework import generics
from .models import User
from .serializers import UserSerializer

# Create your views here.

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# This view only allows GET requests to see all users
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()           # Fetch all users from the DB
    serializer_class = UserSerializer       # Use the translator we built earlier