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


class OrganizationInviteSerializer(serializers.ModelSerializer):
    # TODO: Can potentially use ModelSerializer for this
    # organization = serializers.IntegerField(required=True)
    account_inviter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # invited_email = serializers.EmailField(required=True)

    class Meta:
        model = models.OrganizationInvite
        fields = (
            "organization",
            "account_inviter",
            "invited_email",
            "invited_account",
            "role",
        )
