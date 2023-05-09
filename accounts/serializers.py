from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    role = serializers.CharField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'password')
