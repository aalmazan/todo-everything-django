from rest_framework import permissions, viewsets

from . import models
from . import permissions as org_permissions
from . import serializers


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = models.Organization.objects.none()
    serializer_class = serializers.OrganizationSerializer()
    permission_classes = [permissions.IsAdminUser, org_permissions.IsInOrganization]
