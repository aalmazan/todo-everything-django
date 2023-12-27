from rest_framework import serializers

from . import models


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ("name", "accounts")


class OrganizationPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ("name",)
