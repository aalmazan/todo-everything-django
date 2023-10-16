from rest_framework.serializers import ModelSerializer

from . import models


class AccountSerializer(ModelSerializer):
    class Meta:
        model = models.Account
        fields = ["id", "email"]


class AccountProfileSerializer(ModelSerializer):
    class Meta:
        model = models.AccountProfile
        fields = ["id", "full_name"]
