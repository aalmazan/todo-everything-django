from rest_framework.serializers import ModelSerializer

from . import models


class TodoSerializer(ModelSerializer):
    class Meta:
        model = models.Todo
        fields = [
            "id",
        ]
