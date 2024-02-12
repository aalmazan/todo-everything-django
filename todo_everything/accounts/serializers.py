from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import models


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ["id", "email"]


class AccountRegisterResponseSerializer(TokenObtainPairSerializer):
    pass


class AccountSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ("id", "email")


class AccountProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountProfile
        fields = ["id", "full_name"]


class AccountRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=128, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=models.Account.objects.all(),
                lookup="iexact",
                message=_("A user with that email already exists."),
            )
        ],
    )
    password = serializers.CharField(required=True, min_length=3, write_only=True)
