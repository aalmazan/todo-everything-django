from mixins.models.common import UserStampedModel
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: UserStampedModel):
        return request.user == obj.created_by
