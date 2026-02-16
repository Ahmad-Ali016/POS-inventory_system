from rest_framework import serializers
from .models import Customer, Sale

class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'address']

        extra_kwargs = {
            'password': {'write_only': True}, # Hide password in responses
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        # The .save() method in our model handles the hashing
        return Customer.objects.create(**validated_data)

class SaleReadSerializer(serializers.ModelSerializer):
    # These fields pull data from the related models
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    staff_name = serializers.CharField(source='staff_member.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    unit_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id',
            'sale_date',
            'customer_name',
            'staff_name',
            'product_name',
            'unit_price',
            'quantity_sold',
            'total_price'
        ]