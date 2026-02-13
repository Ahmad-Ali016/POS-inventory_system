from rest_framework import generics, status
from .models import Product
from inventory.serializers import ProductSerializer

from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

# Standard view to Create and List products
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Custom view to handle Stock Adjustments
class StockUpdateView(APIView):
    def post(self, request, pk):
        # 1. Find the product by the ID (pk) provided in the URL
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Get the 'amount' from the Postman request body
        amount = request.data.get('amount', 0)

        # 3. Use our model method to update stock
        success = product.update_stock(int(amount))

        if success:
            return Response({"message": "Stock updated", "new_stock": product.stock})
        else:
            return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)