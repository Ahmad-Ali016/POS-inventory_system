from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Explicitly listing fields for clarity
        fields = ['id', 'name', 'price', 'stock']