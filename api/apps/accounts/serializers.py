from apps.accounts.models import User
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "role",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        django_validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
