from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

User = get_user_model()
POST_STATUS = (
    ('draft', 'Draft'),  # перше в бази друге для відображення
    ('publish', 'Publish'),
)


class PostQuerySet(models.QuerySet):
    def draft(self):
        return self.filter(status='draft')

    def publish(self):
        return self.filter(status='publish')


class PostManager(models.Manager):
    def draft(self):
        return self.get_queryset().draft()

    def publish(self):
        return self.get_queryset().publish()

    def get_queryset(self):
        return PostQuerySet(model=self.model, using=self._db, hints=self._hints)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = RichTextUploadingField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=POST_STATUS, default='draft')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PostManager()

    class Meta:
        default_related_name = 'posts'  # дефолтне імя по якому будуть звертатися зовні
        ordering = ('created',)

    def __str__(self) -> str:
        return f'{self.id}:{self.title}'


class Comment(models.Model):
    author = models.CharField(max_length=60)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # related_name як звертається з
    # модельки пост до кементів
    body = models.TextField()
    status = models.CharField(max_length=20, choices=POST_STATUS, default='draft')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'{self.id}:{self.author}'


class Like(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    session_key = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'session_key',)
