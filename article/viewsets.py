from datetime import datetime

from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from article.filter import PostFilter, CommentFilter
from article.models import Post, Comment, Like
from article.serializers import PostSerializer, CommentSerializer
from core.viewsets import BaseModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(BaseModelViewSet):
    queryset = Post.objects.annotate(like_count=Count("likes"))
    serializer_class = PostSerializer

    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'comments__id']
    ordering = ['created']
    ordering_fields = ['id', 'title', 'author__first_name', 'author__last_name']
    filterset_class = PostFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return (
            qs.prefetch_related('comments')
                .select_related("author")
                .annotate(like_count=Count("likes", distinct=True), comments_count=Count('comments', distinct=True))
        )

    @action(methods=["GET"], detail=False, url_path="top_by_comments")
    def top_by_comments(self, request, *args, **kwargs):
        top_count = int(request.GET.get('top', 10))
        posts = Post.objects.all() \
                    .annotate(like_count=Count("likes", distinct=True), \
                              comments_count=Count("comments", distinct=True)).order_by('-comments_count')[:top_count]
        serializer = PostSerializer(posts, many=True)
        return Response({
            "comments": serializer.data
        })

    @action(methods=["GET"], detail=False, url_path="top_by_likes")
    def top_by_likes(self, request, *args, **kwargs):
        top_count = int(request.GET.get('top', 10))
        posts = Post.objects.all() \
                    .annotate(like_count=Count("likes", distinct=True), \
                              comments_count=Count("comments", distinct=True)).order_by('-like_count')[:top_count]
        serializer = PostSerializer(posts, many=True)
        return Response({
            "posts": serializer.data
        })

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @action(methods=["POST"], detail=True, url_path="do_like")
    def like(self, request, *args, **kwargs):
        session = request.session.session_key
        user_ip = self.get_client_ip(request)
        if not session:
            session = user_ip
        post = self.get_object()
        # user_ip
        existed_like = Like.objects.filter(session_key=session, post=post).first()
        if existed_like:
            existed_like.delete()
        else:
            Like.objects.create(session_key=session, created=datetime.now(), post=post)
        likes = Like.objects.filter(post=post).count()
        return Response({
            "likes": likes
        })


class CommentViewSet(NestedViewSetMixin, BaseModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = CommentFilter

    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data'):
            kwargs['data'].update(self.get_parents_query_dict())
        return super(CommentViewSet, self).get_serializer(*args, **kwargs)
