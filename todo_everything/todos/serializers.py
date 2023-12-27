import logging

from accounts import serializers as accounts_serializers
from organizations import serializers as organizations_serializers
from rest_framework import serializers

from . import models

logger = logging.getLogger(__name__)


class TodoSerializer(serializers.ModelSerializer):
    completed = serializers.DateTimeField(allow_null=True, required=False)
    created_by = accounts_serializers.AccountSerializerPublic(
        read_only=True, required=False
    )
    organization = organizations_serializers.OrganizationPublicSerializer(
        read_only=True, required=False
    )

    class Meta:
        model = models.Todo
        read_only_fields = ["created_by"]
        fields = ["id", "title", "body", "created_by", "completed", "organization"]
        depth = 1


class TodoWriteSerializer(TodoSerializer):
    # Potentially https://drf-rw-serializers.readthedocs.io/en/latest/
    organization_id = serializers.IntegerField(required=False, allow_null=True)

    def get_fields(self):
        print("get fields")
        return super().get_fields()

    def validate_organization_id(self, value):
        # Valid when the value exists in the user's organizations list
        # TODO: Extend to further check organizations that user has write permissions on.
        has_org = self.context.get("request").user.has_organization_access(
            organization=value
        )
        if not has_org:
            logger.info("Invalid organization %s used for Todo creation", value)
            raise serializers.ValidationError("Invalid organization used")
        return value

    def create(self, validated_data):
        if self.context.get("request").user:
            validated_data["created_by"] = self.context.get("request").user
        return super().create(validated_data)

    class Meta:
        model = models.Todo
        read_only_fields = ["created_by"]
        fields = ["id", "title", "body", "created_by", "completed", "organization_id"]
        depth = 1
