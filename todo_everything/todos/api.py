import logging

from django.db.models import Count, Q
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
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
    filterset_fields = [
        "organization",
    ]

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

        # TODO: Somehow put logic into manager? Possibly in user manager
        created_by_self = Q(created_by=self.request.user)
        owned_by_org = self.request.query_params.get("org", None)
        if owned_by_org and isinstance(owned_by_org, int):
            the_filter = Q(organization_id=owned_by_org)
        else:
            the_filter = created_by_self

        return models.Todo.available_objects.filter(the_filter)

    @action(methods=["GET"], detail=False)
    def today(self, request, *args, **kwargs):
        queryset = (models.Todo.todos.for_user(self.request.user)) & (
            models.Todo.todos.started_not_done() | models.Todo.todos.due_today()
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def assigned(self, request, *args, **kwargs):
        queryset = models.Todo.todos.assigned()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def unassigned(self, request, *args, **kwargs):
        queryset = models.Todo.todos.unassigned()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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
        # This potentially causes a hit from another(?) seria   lization.
        serializer = self.read_serializer_class(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TodoOverviewView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # TODO: Probably cache this as it will eventually be an expensive-ish operation.
        created_by_self = Q(created_by=self.request.user)
        owned_by_orgs = Q(organization__in=self.request.user.organizations.all())
        queryset = (
            models.Todo.available_objects.filter(created_by_self | owned_by_orgs)
            .values("organization")
            .annotate(num_todos=Count("id"))
        )
        return Response(data=queryset, status=status.HTTP_200_OK)
