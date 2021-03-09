from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, IsAdminUser


class PostPermission(BasePermission):
    def has_permission(self, request, view):
        # LIST, CREATE
        print(request.method)
        if request.method in SAFE_METHODS:
            return True
        if IsAuthenticated().has_permission(request, view):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if IsAuthenticated().has_permission(request, view) and obj.author == request.user:
            return True
        return False


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and request.method == 'POST' \
                and IsAuthenticated().has_permission(request, view):
            return True
        if IsAdminUser().has_permission(request, view):
            return True
        return False
