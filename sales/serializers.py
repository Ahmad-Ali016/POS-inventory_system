from rest_framework import serializers
from .models import Customer

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