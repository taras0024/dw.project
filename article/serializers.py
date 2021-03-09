from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import serializers

from article.models import Post, Comment
from core.serializers import BaseModelSerializer

User = get_user_model()


class CommentSerializer(BaseModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), source='post'
    )
    class Meta:
        model = Comment
        fields = ('id', 'author', 'body', 'post_id')


class PostSerializer(BaseModelSerializer):

    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='author'
    )

    class Meta:
        model = Post
        fields = ('id', 'author_id', 'slug', 'title', 'body', 'comments_count', 'comments', 'like_count')
