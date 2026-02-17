from rest_framework import generics, status
from .models import Product, Category, Batch
from inventory.serializers import ProductSerializer, CategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Sum


# Create your views here.

# This endpoint only allows POST requests to create a new item
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        category_name = request.data.get('category_name')
        initial_stock = int(request.data.get('stock', 0))
        price = request.data.get('price')
        product_name = request.data.get('name')

        if not category_name:
            return Response({"error": "category_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. Handle Category (Lazy Creation)
                category, _ = Category.objects.get_or_create(name=category_name)

                # 2. Handle Product
                # We use get_or_create in case the product name already exists
                product, created = Product.objects.get_or_create(
                    name=product_name,
                    defaults={'category': category, 'price': price}
                )

                # 3. Handle Initial Stock (Create first Batch)
                if initial_stock > 0:
                    Batch.objects.create(
                        product=product,
                        quantity=initial_stock,
                        cost_price=price,  # Assuming cost=selling for initial setup
                        selling_price=price
                    )

                # 4. Prepare Response
                serializer = self.get_serializer(product)
                return Response({
                    "product": serializer.data,
                    "initial_stock_added": initial_stock,
                    "category_used": category.name,
                    "message": "Product and initial batch created successfully!"
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# This view handles the GET request to list everything in the database
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    # This tells Django HOW to format the data
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# This view handles both GET (list) and POST (create)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StockAlertView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.annotate(
            calculated_stock=Sum('batches__quantity')
        ).order_by('calculated_stock')