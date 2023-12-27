import logging

from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response

from . import models, permissions, serializers

logger = logging.getLogger(__name__)


class TodoViewSet(viewsets.ModelViewSet):
    queryset = models.Todo.objects.none()
    permission_classes = [permissions.IsOwner]
    read_serializer_class = serializers.TodoSerializer
    write_serializer_class = serializers.TodoWriteSerializer

    def get_serializer_class(self):
        print("Serializer action: ", self.action)
        ret = self.read_serializer_class
        if self.action == "create":
            ret = self.write_serializer_class
        return ret

    def get_queryset(self):
        created_by_self = Q(created_by=self.request.user)
        owned_by_org = self.request.GET.get("org", None)
        if owned_by_org and isinstance(owned_by_org, int):
            the_filter = Q(created_by_self | Q(organization_id=owned_by_org))
        else:
            the_filter = Q(created_by_self)

        return models.Todo.objects.filter(the_filter).order_by("-created")

    def create(self, request, *args, **kwargs):
        """
        Custom create method to allow write and read serializers to work on a single request.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Instance now updated on self.instance.
        # Write serializer should have been used.
        self.perform_create(serializer)

        # Used write_serializer's updated data on the read_serializer for creating a response.
        # This potentially causes a hit from another(?) serialization.
        serializer = self.read_serializer_class(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
