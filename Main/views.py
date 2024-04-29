from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from Main.models import Post, Comment, Account
from Main.models import Post, Comment, Account, Activity
from django.contrib.auth.forms import UserCreationForm  
from django.shortcuts import render  
from Main.forms import CommentForm, PostForm
from django.contrib.auth import login, authenticate

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.models import User
 


class MyAccountAndUpdateView(UpdateView): 
    # specify the model you want to use 
    model = Account 

    template_name = "MyAccount.html"
  
    # specify the fields 
    fields = [ 
        "email", 
        "account_name",
        "account_bio"

    ] 
  
    # can specify success url 
    # url to redirect after successfully 
    # updating details 
    success_url = reverse_lazy('home')



def HomePage(request):
    if not request.user.is_authenticated:
        
        context = {}

        return render(request, "home.html", context)
    elif request.user.is_authenticated:
        posts = Post.objects.all().order_by("-created_on")
        context = {"posts": posts, "current_user": request.user}
        return render(request, "UserFeed.html", context)


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'

    

    def get_queryset(self):
        query = self.request.GET.get("q")
        

        if query != None:
            object_list = []
        else:
            object_list = Post.objects.all()

        return object_list

@login_required
def post_index(request):
    posts = Post.objects.all().order_by("-created_on")
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            #current_user = request.user
            if not request.user.is_superuser:
                try:
                    account = Account.objects.get(user_owner=request.user)
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

#this is how votes/activities work
#https://simpleisbetterthancomplex.com/tutorial/2016/10/13/how-to-use-generic-relations.html
@login_required
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

        userAlreadyVoted = post.votes.filter(user=request.user) #this uses the post instance
        thisUserAccount = Account.objects.filter(user_owner=request.user)
        userMadePost = Post.objects.get(pk=pk)  #this uses the post model, responsible for all instances
        userMadePost = (userMadePost.accountname == thisUserAccount)
        


        if not userAlreadyVoted and not userMadePost:
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
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.post = post
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()

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
        user_owner = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        account_name = request.POST.get('account_name')
        account_bio = request.POST.get('account_bio', '')

        account = Account.objects.create(user_owner=request.user, username=username, email=email, account_name=account_name, account_bio=account_bio)
        #account.save
    
    return render(request, 'create_account.html')

def search_account(request):
    query = request.GET.get('q')
    accounts = Account.objects.filter(username__icontains=query)
    return render(request, 'search_account.html', {'users': accounts, 'query': query})

def report_post(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
        post.reported_count += 1
        post.save()
        # Redirect to the detail page of the reported post
        return redirect(reverse('post_detail', kwargs={'pk': post_id, 'action': 1}))  # Assuming 'action' is 1 for post detail
    except Post.DoesNotExist:
        return JsonResponse({'error': 'The specified post does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def report_user(request, user_id):
    user = Account.objects.get(pk=user_id)
    user.reported_count += 1
    user.save()


def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})