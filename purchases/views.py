from rest_framework import generics, status
from .models import Vendor, Supply
from purchases.serializers import VendorSerializer, VendorListSerializer, SupplyHistorySerializer

from rest_framework.views import APIView
from django.db import transaction
from accounts.models import User
from inventory.models import Category, Product, Batch
from rest_framework.response import Response

from decimal import Decimal, InvalidOperation
from accounts.permissions import IsAdmin, IsCashier


# Create your views here.

class VendorListCreateView(generics.ListCreateAPIView):
    permission_classes = [ IsAdmin ]

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class AllVendorsListView(generics.ListAPIView):
    permission_classes = [IsCashier | IsAdmin]

    queryset = Vendor.objects.all().order_by('company_name')  # Alphabetical order
    serializer_class = VendorListSerializer


class ProcessSupplyView(APIView):
    permission_classes = [ IsAdmin ]
    def post(self, request):
        # 1. Capture Data from Request
        vendor_id = request.data.get('vendor_id')
        admin_id = request.data.get('admin_id')
        category_name = request.data.get('category_name')  # Using Name instead of ID
        product_name = request.data.get('product_name')

        try:
            # Use Decimal for financial accuracy; float can cause rounding errors
            qty_received = int(request.data.get('quantity', 0))
            cost_price = Decimal(str(request.data.get('cost_price', 0)))
            selling_price = Decimal(str(request.data.get('selling_price', 0)))
        except (ValueError, TypeError, InvalidOperation):
            return Response({"error": "Invalid quantity or price format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 2. Fetch required related objects (Vendor and Admin)
                # Using get() specifically to trigger DoesNotExist if they are missing
                vendor = Vendor.objects.get(id=vendor_id)
                admin = User.objects.get(id=admin_id)

                # 3. AUTOMATIC CATEGORY: Get or Create by name
                category, cat_created = Category.objects.get_or_create(name=category_name)

                # Add category to Vendor's profile if not already there
                # .add() automatically handles checking for duplicates in ManyToMany fields
                vendor.categories.add(category)

                # 4. SMART PRODUCT: Get or Create
                # If product exists, we use it; if not, we create it with current category/price
                product, prod_created = Product.objects.get_or_create(
                    name=product_name,
                    defaults={
                        'category': category,
                        'price': selling_price,
                    }
                )

                # 5. BATCH CREATION: Track this specific shipment
                batch = Batch.objects.create(
                    product=product,
                    quantity=qty_received,
                    cost_price=cost_price,
                    selling_price=selling_price
                )

                # 6. SUPPLY RECORD: Permanent Receipt
                supply = Supply.objects.create(
                    vendor=vendor,
                    product=product,
                    category=category,
                    order_person=admin,
                    quantity_received=qty_received,
                    cost_price=cost_price
                )

                return Response({
                    "message": "Supply processed successfully!",
                    "details": {
                        "product": product.name,
                        "category": category.name,
                        "category_status": "New" if cat_created else "Existing",
                        "product_status": "New" if prod_created else "Updated",
                        "category_linked": category.name,
                        "batch_id": batch.id,
                        "quantity_added": qty_received,
                        "total_stock": product.total_stock  # Uses the @property
                    }
                }, status=status.HTTP_201_CREATED)

        # 7. SPECIFIC ERROR HANDLING
        except Vendor.DoesNotExist:
            return Response({"error": f"Vendor with ID {vendor_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": f"Admin user with ID {admin_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Catch-all for unexpected database issues
            return Response({"error": f"An unexpected error occurred: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VendorPurchaseHistoryView(generics.ListAPIView):
    permission_classes = [IsCashier | IsAdmin]

    serializer_class = SupplyHistorySerializer

    def get_queryset(self):
        # Start with all supply records, newest first
        queryset = Supply.objects.all().order_by('-supply_date')

        # Optional: Filter by vendor_id if provided in the URL query
        # Example: /api/purchases/history/?vendor_id=1
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id is not None:
            queryset = queryset.filter(vendor_id=vendor_id)

        return queryset