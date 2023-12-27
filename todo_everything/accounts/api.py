import logging

from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from . import models, serializers

logger = logging.getLogger("todo_everything.accounts.api")


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.none()
    serializer_class = serializers.AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["GET"], detail=False)
    def me(self, request, **kwargs):
        user = request.user
        logger.info("User exists: %s", request.user)
        serializer = self.get_serializer(user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AccountProfileViewSet(viewsets.ModelViewSet):
    queryset = models.AccountProfile.available_objects.none()
    serializer_class = serializers.AccountProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountRegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.AccountRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        user = models.Account.objects.create_user(**serializer.validated_data)
        serialized_user = serializers.AccountSerializer(user)
        return Response(status=status.HTTP_201_CREATED, data=serialized_user.data)
