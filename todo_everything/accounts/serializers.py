from rest_framework import serializers

from . import models


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ["id", "email"]


class AccountSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ["id", "email"]


class AccountProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountProfile
        fields = ["id", "full_name"]


class AccountRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=3, write_only=True)
