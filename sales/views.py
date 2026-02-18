from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User
from accounts.permissions import IsCashier, IsAdmin
from inventory.models import Product, Batch
from .models import Customer, Sale
from .serializers import CustomerRegisterSerializer, SaleReadSerializer

from django.contrib.auth.hashers import check_password
from django.db import transaction


# Create your views here.

class RegisterView(generics.CreateAPIView):
    permission_classes = [IsAdmin]

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
    permission_classes = [IsCashier | IsAdmin]

    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer


class ProcessSaleView(APIView):
    permission_classes = [IsCashier | IsAdmin]

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

                # 2. Check total availability using the @property we created
                if product.total_stock < qty_to_buy:
                    return Response(
                        {"error": f"Insufficient stock. Only {product.total_stock} available."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 3. FIFO LOGIC: Deduct from Batches (Oldest First)
                # We filter for batches with quantity > 0 and order by creation date
                available_batches = Batch.objects.filter(
                    product=product,
                    quantity__gt=0
                ).order_by('created_at')

                remaining_to_deduct = qty_to_buy

                for batch in available_batches:
                    if remaining_to_deduct <= 0:
                        break

                    if batch.quantity <= remaining_to_deduct:
                        # Use up this entire batch
                        remaining_to_deduct -= batch.quantity
                        batch.quantity = 0
                        batch.save()
                    else:
                        # Take only what is needed from this batch
                        batch.quantity -= remaining_to_deduct
                        remaining_to_deduct = 0
                        batch.save()

                # 4. Create Sale Record
                total_amount = product.price * qty_to_buy
                sale = Sale.objects.create(
                    customer=customer,
                    staff_member=staff,
                    product=product,
                    quantity_sold=qty_to_buy,
                    total_price=total_amount
                )

                return Response({
                    "message": "Sale completed successfully!",
                    "transaction_id": sale.id,
                    "customer": customer.username,
                    "staff_handler": staff.username,
                    "product": product.name,
                    "quantity": qty_to_buy,
                    "total_price": float(total_amount),
                    "current_stock_left": product.total_stock
                }, status=status.HTTP_201_CREATED)



        except Product.DoesNotExist:

            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "Staff member not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SaleListView(generics.ListAPIView):
    permission_classes = [IsCashier | IsAdmin]
    queryset = Sale.objects.all().order_by('-sale_date')  # Newest sales first
    serializer_class = SaleReadSerializer
