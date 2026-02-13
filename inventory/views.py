from rest_framework import generics, status
from .models import Product, Category
from inventory.serializers import ProductSerializer, CategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

# This endpoint only allows POST requests to create a new item
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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
        # .order_by('stock') puts 0 at the top, then 1, 2, etc.
        return Product.objects.all().order_by('stock')