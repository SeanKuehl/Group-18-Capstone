
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from Main.models import Post, Comment, Account, Activity
from Main.forms import CommentForm, PostForm


# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.models import User
 
class HomePage(TemplateView):
    template_name = 'home.html'


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Post.objects.filter(
            Q(post_title__icontains=query) | Q(username__icontains=query)
        )
        return object_list

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

#this is how votes/activities work
#https://simpleisbetterthancomplex.com/tutorial/2016/10/13/how-to-use-generic-relations.html
def post_detail(request, pk, action):
    post = Post.objects.get(pk=pk)
    upvoteAction = 1
    downvoteAction = 2

    #are they trying to vote twice?
    #thisUser = User.objects.filter(id = request.user.id)
    #print(thisUser)

    if request.user.is_anonymous:
        #if not signed in, they can't vote
        pass
    else:

        userAlreadyVoted = post.votes.filter(user=request.user)


        if not userAlreadyVoted:
            if action == upvoteAction:
                post.votes.create(activity_type=Activity.UP_VOTE, user=request.user)
            elif action == downvoteAction:
                post.votes.create(activity_type=Activity.DOWN_VOTE, user=request.user)
            else:
                pass

        else:
            #they already voted, don't let them vote again
            pass

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

    postUpvotes = post.votes.filter(activity_type=Activity.UP_VOTE).count()
    postDownvotes = post.votes.filter(activity_type=Activity.DOWN_VOTE).count()

    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
        "upvotes": postUpvotes,
        "downvotes": postDownvotes,
    }

    return render(request, "detail.html", context)



    

    
    
    
def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        account_name = request.POST.get('account_name')
        account_bio = request.POST.get('account_bio', '')

        account = Account.objects.create(username=username, email=email, account_name=account_name, account_bio=account_bio)
        return redirect('home')
    return render(request, 'create_account.html')

def search_account(request):
    query = request.GET.get('q')
    accounts = Account.objects.filter(username__icontains=query)
    return render(request, 'search_account.html', {'users': accounts, 'query': query})

