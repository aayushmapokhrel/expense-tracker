from rest_framework import serializers
from .models import ExpenseIncome
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class ExpenseIncomeSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
        )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ExpenseIncome
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token
