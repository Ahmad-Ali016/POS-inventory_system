from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Fields we want to see/send in Postman
        fields = ['id', 'username', 'email', 'role', 'password']
        # Hide the password in GET responses for security
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use create_user to ensure the password gets hashed (not saved as plain text)
        return User.objects.create_user(**validated_data)