from rest_framework import permissions, viewsets

from . import models
from . import permissions as org_permissions
from . import serializers


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = models.Organization.objects.none()
    serializer_class = serializers.OrganizationSerializer
    # Can set permissions using bitwise or
    # https://www.django-rest-framework.org/api-guide/permissions/#setting-the-permission-policy
    # Need the trailing comma in the tuple in order to keep it a
    # tuple/iterable as required by permissions_classes.
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser | org_permissions.IsInOrganization,
    )

    def get_queryset(self):
        return self.request.user.organizations.all()
