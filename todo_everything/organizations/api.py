from django.db.models import Q
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


class OrganizationInviteViewSet(viewsets.ModelViewSet):
    queryset = models.OrganizationInvite.objects.none()
    serializer_class = serializers.OrganizationInviteSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser | org_permissions.IsOrganizationAdmin,
    ]

    def get_queryset(self):
        is_inviter = Q(account_inviter=self.request.user)
        # Only get instances where the user was already attached.
        # Checking invites via current user email would be dangerous since a
        # user can change their email at any time and query against current
        # invites for that email.
        is_invited = Q(invited_account=self.request.user)
        return self.queryset.filter(is_inviter | is_invited)
