from accounts import serializers as accounts_serializers
from organizations import serializers as organizations_serializers
from rest_framework import serializers

from . import models


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
    # TODO: Change from `IntegerField` to `CharField` if changing to a different key structure.
    organization = serializers.IntegerField()

    def get_fields(self):
        print("get fields")
        return super().get_fields()

    def validate_organization_id(self, value):
        print("TodoWriteSerializer validate_org:", value)

        # Valid when the value exists in the user's organizations list
        # TODO: Extend to further check organizations that user has write permissions on.
        has_org = (
            self.context.get("request").user.organizations.filter(pk=value).exists()
        )
        if not has_org:
            raise serializers.ValidationError("Invalid organization used")
        return value

    def create(self, validated_data):
        if self.context.get("request").user:
            validated_data["created_by"] = self.context.get("request").user

        # When creating a `Todo` we use `organization_id`, so we're remapping
        # that field here.
        organization_id = validated_data.pop("organization", None)
        if organization_id:
            validated_data["organization_id"] = organization_id

        return super().create(validated_data)

    class Meta:
        model = models.Todo
        read_only_fields = ["created_by"]
        fields = ["id", "title", "body", "created_by", "completed", "organization"]
        depth = 1
