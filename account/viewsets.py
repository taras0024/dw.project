from django.contrib.auth import get_user_model
from rest_framework import viewsets

from core.viewsets import BaseModelViewSet
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
