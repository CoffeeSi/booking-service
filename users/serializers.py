from typing import Any

from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]
