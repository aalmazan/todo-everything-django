from rest_framework import viewsets

from . import models, serializers


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer


class AccountProfileViewSet(viewsets.ModelViewSet):
    queryset = models.AccountProfile.objects.all()
    serializer_class = serializers.AccountProfileSerializer
