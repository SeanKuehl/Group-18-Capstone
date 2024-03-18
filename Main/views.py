from django.http import HttpResponseRedirect
from django.shortcuts import render
from Main.models import Post, Comment
from Main.forms import CommentForm, PostForm

# Create your views here.
from django.views.generic.base import TemplateView
 
class HomePage(TemplateView):
    template_name = 'home.html'

def post_index(request):
    posts = Post.objects.all().order_by("-created_on")
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(
                username = form.cleaned_data["username"],
                post_title = form.cleaned_data["post_title"],
                post_community = form.cleaned_data["post_community"],
                post_body = form.cleaned_data["post_body"]
            )
            post.save()
            return HttpResponseRedirect(request.path_info)
    context = {
        "posts": posts,
        "form": PostForm(),
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
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }

    return render(request, "detail.html", context)
