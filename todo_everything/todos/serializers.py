from accounts import serializers as accounts_serializers
from rest_framework.serializers import ModelSerializer

from . import models, tasks


class TodoSerializer(ModelSerializer):
    created_by = accounts_serializers.AccountSerializer(allow_null=True)

    def save(self, **kwargs):
        user = self.context.get("request").user  # type: ignore
        obj = super().save(created_by=user, **kwargs)
        tasks.task_todo.delay(obj.id)
        return obj

    class Meta:
        model = models.Todo
        read_only_fields = ["created_by", "completed"]
        fields = ["id", "title", "body", "created_by", "completed"]
        depth = 1
