from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import serializers

from article.models import Post, Comment
from core.serializers import BaseModelSerializer

User = get_user_model()


class CommentSerializer(BaseModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'body')


class PostSerializer(BaseModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='author'
    )

    like_count = serializers.IntegerField()

    # TODO serializer author

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author_id', 'slug', 'title', 'body', 'comments', 'like_count')
