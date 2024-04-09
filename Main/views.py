from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from Main.models import Post, Comment, Account
from Main.forms import CommentForm, PostForm


# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.db.models import Q
 
class HomePage(TemplateView):
    template_name = 'home.html'


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Post.objects.filter(
            Q(post_title__icontains=query) | Q(accountname__username__icontains=query)
        )
        return object_list

@login_required
def post_index(request):
    posts = Post.objects.all().order_by("-created_on")
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            current_user = request.user
            if not current_user.is_superuser:
                try:
                    account = Account.objects.get(username=current_user.username)
                except Account.DoesNotExist:
                    # Handle the case where the Account instance doesn't exist
                    # Redirect to a page where the user can create their account
                    return HttpResponseRedirect('/create-account')
            else:
                # If the user is a superuser, set the account to None
                account = None
                    
            post = form.save(commit=False)
            post.accountname = account
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()

    context = {
        "posts": posts,
        "form": form,
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

def user_account(request, user_id):
    if user_id == 0:
        # For the placeholder superuser ID, display all posts
        posts = Post.objects.all()
        return render(request, 'account_page.html', {'account_name': "Superuser", 'posts': posts})
    else:
        # For regular users, retrieve their account and associated posts
        account = get_object_or_404(Account, pk=user_id)
        if request.user.is_superuser:
            return render(request, 'account_page.html', {'account_name': "Superuser's Account", 'posts': posts})
        else:
            posts = Post.objects.filter(accountname=account)
            return render(request, 'account_page.html', {'account': account, 'posts': posts})


    
def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        account_name = request.POST.get('account_name')
        account_bio = request.POST.get('account_bio', '')

        account = Account.objects.create(username=username, email=email, account_name=account_name, account_bio=account_bio)
        #account.save
    
    return render(request, 'create_account.html')

def search_account(request):
    query = request.GET.get('q')
    accounts = Account.objects.filter(username__icontains=query)
    return render(request, 'search_account.html', {'users': accounts, 'query': query})
