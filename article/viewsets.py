from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from article.filter import PostFilter, CommentFilter
from article.models import Post, Comment
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
                .annotate(like_count=Count("likes"))
        )


    @action(methods=['POST'], detail=True, url_path='do_like')
    def like(self, request, *args, **kwargs):
        session = request.session.session_key

        # TODO зробити Лайк з використанням сешин кей або IP адреси клієнта
        return Response('')


# TODO підключити джанго-фільтер, зробити фільтрування постів, коментарів
# підключити drf_yasg,

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



