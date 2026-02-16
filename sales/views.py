from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User
from inventory.models import Product
from .models import Customer, Sale
from .serializers import CustomerRegisterSerializer, SaleReadSerializer

from django.contrib.auth.hashers import check_password
from django.db import transaction


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


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer


class ProcessSaleView(APIView):
    def post(self, request):
        # 1. Get IDs from the Postman request
        customer_id = request.data.get('customer_id')
        product_id = request.data.get('product_id')
        staff_id = request.data.get('staff_id')
        qty_to_buy = int(request.data.get('quantity', 0))

        try:
            # We wrap the logic in an atomic block
            with transaction.atomic():
                # 1. Fetch objects
                product = Product.objects.get(id=product_id)
                customer = Customer.objects.get(id=customer_id)
                staff = User.objects.get(id=staff_id)  # Now specifically checked

                # 2. Stock
                if not product.update_stock(-qty_to_buy):
                    return Response(
                        {"error": f"Insufficient stock. Only {product.stock} available."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 3. Calculate and Create
                total = product.price * qty_to_buy
                sale = Sale.objects.create(
                    customer=customer,
                    staff_member=staff,
                    product=product,
                    quantity_sold=qty_to_buy,
                    total_price=total
                )

                return Response({
                    "message": "Sale completed successfully!",
                    "transaction_id": sale.id,
                    "product/item": product.name,
                    "unit_price": float(product.price),
                    "number_of_units": qty_to_buy,
                    "total_price": float(total),
                    "remaining_stock": product.stock
                }, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "Staff member not found"}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SaleListView(generics.ListAPIView):
    queryset = Sale.objects.all().order_by('-sale_date') # Newest sales first
    serializer_class = SaleReadSerializer