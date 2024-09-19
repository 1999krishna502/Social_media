from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =  '__all__'
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])  # Extract groups data if present
        permissions_data = validated_data.pop('user_permissions', [])  # Extract permissions data if present

        user = get_user_model().objects.create_user(**validated_data)

        # Set groups and user_permissions separately
        user.groups.set(groups_data)
        user.user_permissions.set(permissions_data)

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['user'] = CustomUserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

