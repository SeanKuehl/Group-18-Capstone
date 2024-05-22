from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from Main.models import Post, Comment, Activity
from Main.forms import CustomUserCreationForm  
from django.shortcuts import render  
from Main.forms import CommentForm, PostForm
from Accounts.models import CustomUser
from django.contrib.auth import login, authenticate

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.db.models import Q

 


class MyAccountAndUpdateView(UpdateView): 
    # specify the model you want to use 
    model = CustomUser

    template_name = "MyAccount.html"
  
    # specify the fields 
    fields = [ 
        "email", 
        "username",
        "account_bio",

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
        context = {"posts": posts, "current_user": request.user, "admin": request.user.admin_status}
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
                
                account = request.user
                
            else:
                # If the user is a superuser, set the account to None
                account = None
                    
            post = form.save(commit=False)
            post.accountname = account
            post.save()

            # Process tags separately
            tags_input = request.POST.get('tags')
            if tags_input:
                # Split the tags input string into individual tags
                tags_list = tags_input.split(',')
                for tag_name in tags_list:
                    # Remove leading and trailing spaces from each tag
                    tag_name = tag_name.strip()
                    tag, created = post.tags.get_or_create(name=tag_name)
                    # Add the tag to the post
                    post.tags.add(tag)

            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()

     # Get existing tags from all posts
    existing_tags = []
    for post in posts:
        existing_tags.extend(post.tags.values_list('name', flat=True))

    context = {
        "posts": posts,
        "form": form,
        "existing_tags": existing_tags,
    }

    return render(request, "index.html", context)



def remove_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    context = {}
    return render(request, "post_removed.html", context)


def remove_account(request, pk):
    account = Account.objects.get(pk=pk)
    account.delete()
    context = {}
    return render(request, "account_removed.html", context)



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
        thisUserAccount = request.user
        userMadePost = Post.objects.get(accountname=request.user, pk=pk)  #this uses the post model, responsible for all instances
        userMadePost = (userMadePost.accountname == thisUserAccount.username)
        


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
        return render(request, 'account_page.html', {'account': request.user, 'posts': posts})
    else:
        # For regular users, retrieve their account and associated posts
        account = CustomUser.objects.get(pk=user_id)
        if request.user.is_superuser:
            return render(request, 'account_page.html', {'account': request.user, 'posts': posts})
        else:
            posts = Post.objects.filter(accountname=account)
            return render(request, 'account_page.html', {'account': account, 'posts': posts})


    


def search_account(request):
    query = request.GET.get('q')

    if query == None:
        accounts = []
    else:
        accounts = CustomUser.objects.filter(username__icontains=query)

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

    try:
        
        user = get_object_or_404(CustomUser, pk=user_id)
        user.reported_count += 1
        user.save()
        # Redirect to the detail page of the reported post
        return redirect(reverse_lazy('home'))  
    except Post.DoesNotExist:
        return JsonResponse({'error': 'The specified post does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


    
    


def SignUp(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def get_existing_tags(request):
    # Get all existing tags from the posts
    existing_tags = list(Post.objects.values_list('tags__name', flat=True).distinct())
    return JsonResponse(existing_tags, safe=False)
        
