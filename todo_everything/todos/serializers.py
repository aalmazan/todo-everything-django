from rest_framework import serializers

from . import models, tasks


class TodoSerializer(serializers.ModelSerializer):
    completed = serializers.DateTimeField(allow_null=True, required=False)

    def save(self, **kwargs):
        user = self.context.get("request").user  # type: ignore
        obj = super().save(created_by=user, **kwargs)
        tasks.task_todo.delay(obj.id)
        return obj

    class Meta:
        model = models.Todo
        read_only_fields = ["created_by"]
        fields = ["id", "title", "body", "created_by", "completed"]
        depth = 1
