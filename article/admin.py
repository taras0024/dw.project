from django.contrib import admin
from django.db.models import Count

from article.models import Post, Comment, Like


# from article import models as article_models  == from article.models import *


# виводить коменти під постами в адмінці при їх редагуванні
class CommentAdminModelInLine(admin.TabularInline):
    model = Comment
    extra = 1


class LikeAdminModelInLine(admin.TabularInline):
    model = Like
    extra = 1  # скільки вивести пустих полів якшо 0 то буде просто кнопка add

    # def has_change_permission(self, request, obj) -> bool:
    #     return False

    # def has_add_permission(self, request, obj) -> bool:
    #     return False


@admin.register(Post)  # == admin.site.register(Post, PostAdminModel)
class PostAdminModel(admin.ModelAdmin):
    inlines = [
        CommentAdminModelInLine,  # CommentAdminModelInLine
        LikeAdminModelInLine,  # LikeAdminModelInLine
    ]
    list_display = ('id', 'title', 'author', 'created', 'user_name', 'like_count')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created',)  # default sorting
    list_filter = ('status', 'created')  # create filter in admin

    def user_name(self, obj):  # created new field of user in admin
        return obj.author.username

    def get_queryset(self, request):  # ?створено для оптимізації терміналу?
        qs = super().get_queryset(request)
        return (
            qs.prefetch_related('comments')
                .select_related("author")
                .annotate(like_count=Count("likes"))
        )

    def like_count(self, obj):
        return obj.like_count
        # return obj.likes.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'body', 'status')
    list_filter = ('created', 'updated',)
