from django_filters import rest_framework as filters
from . models import  Post, Comment
from django.contrib.auth.models import User


class PostFilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = ['author', 'title', 'body', 'status']


class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = ['post', 'status']


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']