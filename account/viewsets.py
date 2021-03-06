from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from article.filter import UserFilter
from article.models import Like, Post, Comment
from article.serializers import PostSerializer
from core.viewsets import BaseModelViewSet
from .permissions import UserPermission

from .serializers import UserSerializer
from rest_framework.decorators import permission_classes

User = get_user_model()


class UserViewSet(BaseModelViewSet):
    permission_classes = [UserPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_classes = {
        "posts": PostSerializer
    }
    filterset_class = UserFilter

    @action(methods=['GET'], detail=True, url_path='posts', permission_classes=[AllowAny])
    def posts(self, request, *args, **kwargs):
        user = self.get_object()
        data = user.posts.all().annotate(like_count=Count("likes"))
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

