import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models, permissions, serializers

logger = logging.getLogger("todo_everything.todos.api")


class TodoViewSet(viewsets.ModelViewSet):
    queryset = models.Todo.objects.none()
    serializer_class = serializers.TodoSerializer
    permission_classes = [permissions.IsOwner]

    def get_queryset(self):
        return models.Todo.objects.filter(created_by=self.request.user).order_by("pk")

    @action(detail=True, methods=["POST"])
    def complete(self, request, pk=None):
        logger.info("Completing TODO item: pk=%s", pk)
        todo = self.get_object()  # type: models.Todo
        todo.complete()
        return Response(self.get_serializer(todo).data)

    @action(detail=True, methods=["POST"])
    def uncomplete(self, request, pk=None):
        todo = self.get_object()  # type: models.Todo
        todo.uncomplete()
        return Response(self.get_serializer(todo).data)
