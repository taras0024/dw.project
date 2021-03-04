from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Post


# Create your views here.

# def hello_world(request):
#     return HttpResponse('<h1>Hello World</h1>')


class PostListView(ListView):
    queryset = Post.objects.publish()
    template_name = 'article/index.html'

    def get_context_data(self, **kwargs):
        response = super().get_context_data(**kwargs)
        response["a"] = 100
        return response


class PostDetailView(DetailView):
    model = Post
    template_name = 'article/post_detail.html'
