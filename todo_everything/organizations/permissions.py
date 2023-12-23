from logging import getLogger

from rest_framework import permissions

from . import models

logger = getLogger(__name__)


class IsInOrganization(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: models.Organization):
        has_user = request.user
        is_org_user = request.user.organizations.filter(pk=obj.pk).exists()
        return has_user and is_org_user


class IsOrganizationAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.organizations.filter(pk=obj.pk).exists()
