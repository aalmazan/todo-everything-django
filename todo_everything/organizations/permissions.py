from logging import getLogger

from rest_framework import permissions

from . import models

logger = getLogger(__name__)


class IsInOrganization(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: models.Organization):
        return request.user and request.user.organizations.filter(pk=obj.pk).exists()


class IsOrganizationAdmin(permissions.BasePermission):
    role = models.ORGANIZATION_ADMIN

    def has_permission(self, request, view):
        # TODO: Enforce this structure when using this permissions class.
        #   i.e. `request.data.organization` must exist, but should probably be configurable.
        organization_id = request.data.get("organization", None)
        if not organization_id:
            raise ValueError("organization must be provided in request data")
        return request.user and request.user.organizations.filter(
            organizationaccounts__organization=organization_id,
            organizationaccounts__role=self.role,
        )

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.organizations.filter(pk=obj.pk).exists()
