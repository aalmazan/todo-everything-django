import logging

from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from . import models
from . import permissions as todo_permissions
from . import serializers

logger = logging.getLogger(__name__)


class TodoViewSet(viewsets.ModelViewSet):
    queryset = models.Todo.objects.none()
    permission_classes = [permissions.IsAuthenticated, todo_permissions.IsOwner]
    read_serializer_class = serializers.TodoSerializer
    write_serializer_class = serializers.TodoWriteSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return self.write_serializer_class
        return self.read_serializer_class

    def get_queryset(self):
        """
        Only show objects that are owned by the user and/or the org provided
        in the query params.
        """
        if not self.request.user.is_active:
            # Return the base queryset (should be none or something public-ish)
            return self.queryset

        created_by_self = Q(created_by=self.request.user)
        owned_by_org = self.request.GET.get("org", None)
        if owned_by_org and isinstance(owned_by_org, int):
            the_filter = Q(created_by_self | Q(organization_id=owned_by_org))
        else:
            the_filter = Q(created_by_self)

        return models.Todo.available_objects.filter(the_filter).order_by("-created")

    def create(self, request, *args, **kwargs):
        """
        Custom create method to allow write and read serializers to work on a single request.
        """
        # This serializer is based on the `self.action` of the request.
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
