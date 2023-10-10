from rest_framework import viewsets

from . import models, serializers


class TodoViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer
