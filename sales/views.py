from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerRegisterSerializer

from django.contrib.auth.hashers import check_password


# Create your views here.

class RegisterView(generics.CreateAPIView):
    # Use the Customer model, NOT the authtoken User
    queryset = Customer.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CustomerRegisterSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            # 1. Look for the customer in your specific table
            customer = Customer.objects.get(username=username)

            # 2. Manually check if the provided password matches the hash
            if check_password(password, customer.password):
                # Success!
                return Response({
                    "message": f"Welcome {customer.first_name}, you are logged in!",
                    "customer_id": customer.id,
                    "email": customer.email
                }, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

