from rest_framework import serializers
from purchases.models import Vendor, Supply


class VendorSerializer(serializers.ModelSerializer):
    category_names = serializers.SlugRelatedField(
        source='categories',
        many=True,
        read_only=True,
        slug_field='name'
    )
    admin_username = serializers.CharField(source='registered_by.username', read_only=True)

    class Meta:
        model = Vendor
        fields = [
            'id',
            'registered_by',  # Pass the User ID here
            'admin_username',
            'company_name',
            'contact_person',
            'email',
            'phone_number',
            'address',
            'categories',
            'category_names'
        ]

class VendorListSerializer(serializers.ModelSerializer):
    category_names = serializers.SlugRelatedField(
        source='categories',
        many=True,
        read_only=True,
        slug_field='name'
    )
    admin_name = serializers.CharField(source='registered_by.username', read_only=True)

    class Meta:
        model = Vendor
        fields = [
            'id',
            'company_name',
            'contact_person',
            'email',
            'phone_number',
            'address',
            'admin_name',
            'category_names',
            'date_created'
        ]

class SupplyHistorySerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.company_name')
    product_name = serializers.ReadOnlyField(source='product.name')
    category_name = serializers.ReadOnlyField(source='category.name')
    admin_name = serializers.ReadOnlyField(source='order_person.username')

    class Meta:
        model = Supply
        fields = [
            'id',
            'supply_date',
            'vendor_name',
            'product_name',
            'category_name',
            'quantity_received',
            'cost_price',
            'admin_name'
        ]