from accounts import serializers as accounts_serializers
from rest_framework import serializers

from . import models


class TodoSerializer(serializers.ModelSerializer):
    completed = serializers.DateTimeField(allow_null=True, required=False)
    created_by = accounts_serializers.AccountSerializerPublic(
        read_only=True, required=False
    )

    def save(self, **kwargs):
        user = self.context.get("request").user  # type: ignore
        obj = super().save(created_by=user, **kwargs)
        return obj

    class Meta:
        model = models.Todo
        read_only_fields = ["created_by"]
        fields = ["id", "title", "body", "created_by", "completed"]
        depth = 1
