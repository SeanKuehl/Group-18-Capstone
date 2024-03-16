from django.http import HttpResponseRedirect
from django.shortcuts import render
from Main.models import Post, Comment

# Create your views here.
from django.views.generic.base import TemplateView
 
class HomePage(TemplateView):
    template_name = 'home.html'

def post_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "index.html", context)

def post_tag(request, tag):
    posts = Post.objects.filter(
        tags__name__contains=tag
    ).order_by("-created_on")
    context = {
        "tag": tag,
        "posts": posts,
    }
    return render(request, "tag.html", context)

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
    }

    return render(request, "detail.html", context)
