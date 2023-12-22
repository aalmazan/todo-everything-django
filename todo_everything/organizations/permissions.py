from rest_framework import permissions

from . import models


class IsInOrganization(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: models.Organization):
        # TODO: Check is part of org
        return request.user and request.user == obj
