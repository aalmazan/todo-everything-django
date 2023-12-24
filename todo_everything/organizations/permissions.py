from logging import getLogger

from rest_framework import permissions

from . import models

logger = getLogger(__name__)


class IsInOrganization(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: models.Organization):
        return request.user and request.user.organizations.filter(pk=obj.pk).exists()


class IsOrganizationAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.organizations.filter(pk=obj.pk).exists()
