from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    # This field shows the name of the category in the response for convenience
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        # Explicitly listing fields for clarity
        fields = ['id', 'name', 'price', 'stock', 'category', 'category_name']
        read_only_fields = ['id', 'category_name']

