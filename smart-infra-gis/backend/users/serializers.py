from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'city', 'department', 'phone', 'is_verified']
        read_only_fields = ['id', 'is_verified']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'city', 'department', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user