from rest_framework.serializers import ModelSerializer

from . import models, tasks


class TodoSerializer(ModelSerializer):
    def save(self, **kwargs):
        user = self.context.get("request").user
        obj = super().save(created_by=user, **kwargs)
        tasks.task_todo.delay(obj.id)
        return obj

    class Meta:
        model = models.Todo
        fields = ["id", "title", "body"]
