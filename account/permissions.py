from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


User = get_user_model()


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj: User):
        # LIST, CREATE
        if request.method in SAFE_METHODS:
            return True

        return obj.id == request.user.id