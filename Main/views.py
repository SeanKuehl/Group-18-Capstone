import requests

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from Main.models import Post, Comment, Activity, League, LeagueMembership, Team, Match, UserReview, RegisteredBusiness, DiscountOffer
from Main.forms import CustomUserCreationForm, DiscountOfferForm
from django.shortcuts import render  
from Main.forms import CommentForm, PostForm, LeagueForm, TeamForm, MatchForm, UserReviewForm, DiscountOfferForm

from Accounts.models import CustomUser
from django.contrib.auth import login, authenticate, get_user_model
from django.utils.safestring import mark_safe
from notifications.models import Notification
from .filters import contains_hate_speech, contains_curse_words

import logging

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.db.models import Q, Count

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

            if contains_hate_speech(post.post_body) or contains_curse_words(post.post_body) or contains_hate_speech(post.post_title) or contains_curse_words(post.post_title) or contains_hate_speech(post.post_community) or contains_curse_words(post.post_community):
                return HttpResponse("Your post contains inappropriate content. Please review and try again.") 

            tags_input = request.POST.get('tags')
            if tags_input:
                tags_list = tags_input.split(',')
                for tag_name in tags_list:
                    tag_name = tag_name.strip()
                    if contains_hate_speech(tag_name) or contains_curse_words(tag_name):
                        return HttpResponse("One or more tags contain inappropriate content. Please review and try again.")

            post.save()

            # Extract usernames mentioned in the post content
            mentioned_usernames = [word[1:] for word in post.post_body.split() if word.startswith('@')]
            
            # Notify mentioned users
            User = get_user_model()  # Get the custom user model
            for username in mentioned_usernames:
                try:
                    mentioned_user = User.objects.get(username=username)
                    post_url = reverse('post_detail', kwargs={'pk': post.pk, 'action': 0})
                    notification_text = f'You were mentioned in a post "{post.post_title}" by {request.user.username}.'
                    notification_text += f' Click <a href="{post_url}">here</a> to view the post.'
                    #lets the hyperlink show up
                    notification_text = mark_safe(notification_text)

                    Notification.objects.create(
                        user=mentioned_user,
                        text=notification_text
                    )
                except User.DoesNotExist:
                    pass

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
        
        postAuthor = post.accountname
        currentUser = request.user.username

        userMadePost = (postAuthor == currentUser)
        
        if not userAlreadyVoted and not userMadePost:
            if action == upvoteAction:
                post.votes.create(activity_type=Activity.UP_VOTE, user=request.user)
                notification_text = f'{request.user.username} upvoted your post: "{post.post_title}".'
            elif action == downvoteAction:
                post.votes.create(activity_type=Activity.DOWN_VOTE, user=request.user)
                notification_text = f'{request.user.username} downvoted your post: "{post.post_title}".'
            else:
                pass

            # Save the notification

            if action in [upvoteAction, downvoteAction]:
                Notification.objects.create(
                    user = post.accountname,
                    text = notification_text
                )

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

            # Check for hate speech and curse words
            if contains_hate_speech(comment.body) or contains_curse_words(comment.body):
                return HttpResponse("Your comment contains inappropriate content. Please review and try again.")
            
            comment.save()

            # Code for notif if you mention someone

            # Extract usernames mentioned in the comment
            mentioned_usernames = [word[1:] for word in comment.body.split() if word.startswith('@')]
            
            # Notify mentioned users
            User = get_user_model()  # Get the custom user model
            for username in mentioned_usernames:
                try:
                    mentioned_user = User.objects.get(username=username)
                    post_url = reverse('post_detail', kwargs={'pk': comment.post.pk, 'action': 0})
                    notification_text = f'You were mentioned in a comment by {request.user.username}: "{comment.body}".'
                    notification_text += f' Click <a href="{post_url}">here</a> to view the post.'
                    notification_text = mark_safe(notification_text)

                    Notification.objects.create(
                        user=mentioned_user,
                        text=notification_text
                    )
                except User.DoesNotExist:
                    pass

            # Create notification
            Notification.objects.create(
                user=post.accountname,
                text=f'{comment.author} commented on your post: "{post.post_title}"'
            )

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
            #this is where most regular users will go 
            posts = Post.objects.filter(accountname=account)

            form = UserReviewForm()
            if request.method == "POST":
                form = UserReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.author = request.user.username
                    review.user_reviewed = request.user
                    review.save()
                    return HttpResponseRedirect(request.path_info)
            else:
                form = UserReviewForm()

            reviews_on_this_user = UserReview.objects.filter(user_reviewed=account)

            return render(request, 'account_page.html', {'account': account, 'posts': posts, 'form': form, 'reviews': reviews_on_this_user})


    


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



def validate_business_number(business_num):
    #using the Government of Canada's ISED Corporations API


    #https://apigateway-passerelledapi.ised-isde.canada.ca/corporations/api/v1/corporations/106679285.json?lang=eng
    #note: API key SHOULD NOT be in plain text
    language = 'eng'
    url = 'https://apigateway-passerelledapi.ised-isde.canada.ca/corporations/api/v1/corporations/'+business_num+'.json?lang='+language+''

    response = requests.get(url, headers={"accept": "application/json", "user-key": settings.API_KEY})
    returned_json = response.json() 

    #check for invalid response code first

    if response.status_code == 200:

        if type(returned_json[0]) == dict:
            #it is a valid business
            return True
        else:
            #it is not a valid business
            return False
        
    else:
        return False



def register_business_number(request):
    error = False

    if request.method == 'POST':
        business_number = request.POST['business_number']

        if validate_business_number(str(business_number)) == True:
            #create it registered to this user
            existing_business = RegisteredBusiness.objects.filter(associated_user=request.user, business_number=int(business_number))

            if not existing_business:
                new_business = RegisteredBusiness.objects.create(associated_user=request.user, business_number=int(business_number))
                new_business.save()
                #it worked, redirect to home
                return redirect('home')
            
            else:
                error = True

                context = {
                    "error": error,
                }
        
                return render(request, "register_business.html", context)

        else:
            #set error and return to the same screen
            error = True

            context = {
                "error": error,
            }
    
            return render(request, "register_business.html", context)
        

    else:
        context = {
                "error": error,
            }
    
        return render(request, "register_business.html", context)
    



def view_discounts_page(request):
    user_is_business = False
    this_business = RegisteredBusiness.objects.get(associated_user=request.user)
    offers = DiscountOffer.objects.all()

    if this_business:
        user_is_business = True

    form = DiscountOfferForm()
    if request.method == "POST":
        form = DiscountOfferForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)
            discount.author = request.user.username
            discount.associated_business = this_business
            discount.save()

            context = {
                "is_business": user_is_business,
                "form": form,
                "offers": offers,
            }

            return render(request, "view_discounts.html", context)
        
    context = {
                "is_business": user_is_business,
                "form": form,
                "offers": offers,
            }

    return render(request, "view_discounts.html", context)
        

@login_required
def create_league(request):
    if request.method == 'POST':
        form = LeagueForm(request.POST)
        if form.is_valid():
            league = form.save(commit=False)
            league.owner = request.user
            league.team_league = form.cleaned_data['team_league']
            league.save()
            LeagueMembership.objects.create(player=request.user, league=league)
            return redirect('league_detail', league_id=league.id)
    else:
        form = LeagueForm()
    return render(request, 'leagues/create_league.html', {'form': form})

@login_required
def join_league(request, league_id):
    league = get_object_or_404(League, id=league_id)
    if not LeagueMembership.objects.filter(player=request.user, league=league).exists():
        LeagueMembership.objects.create(player=request.user, league=league)
    return redirect('league_detail', league_id=league.id)

@login_required
def leave_league(request, league_id):
    league = get_object_or_404(League, id=league_id)
    membership = LeagueMembership.objects.filter(player=request.user, league=league).first()
    if membership:
        membership.delete()
    return redirect('league_list')

@login_required
def delete_league(request, league_id):
    league = get_object_or_404(League, id=league_id, owner=request.user)
    league.delete()
    return redirect('league_list')

@login_required
def league_list(request):
    leagues = League.objects.all()
    return render(request, 'leagues/league_list.html', {'leagues': leagues})

@login_required
def league_detail(request, league_id):
    league = get_object_or_404(League, id=league_id)
    members = league.members.all()
    teams = Team.objects.filter(league=league).annotate(num_members=Count('members')) if league.team_league else None
    matches = Match.objects.filter(league=league)

    if request.method == 'POST':
        if request.user == league.owner:
            form = LeagueForm(request.POST, instance=league)
            if form.is_valid():
                form.save()
                return redirect('league_detail', league_id=league.id)
    else:
        form = LeagueForm(instance=league)

    return render(request, 'leagues/league_detail.html', {'league': league, 'members': members, 'teams': teams, 'matches': matches, 'form': form})

@login_required
def update_league(request, league_id):
    league = get_object_or_404(League, id=league_id)
    if request.user != league.owner:
        return redirect('league_detail', league_id=league.id)

    if request.method == 'POST':
        form = LeagueForm(request.POST, instance=league)
        if form.is_valid():
            form.save()
            return redirect('league_detail', league_id=league.id)

    return render(request, 'leagues/league_detail.html', {'league': league, 'members': league.members.all(), 'form': form})

@login_required
def create_team(request, league_id):
    league = get_object_or_404(League, id=league_id)
    if not league.team_league:
        return redirect('league_detail', league_id=league.id)

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.league = league
            team.save()
            form.save_m2m()
            return redirect('league_detail', league_id=league.id)
    else:
        form = TeamForm()

    return render(request, 'leagues/create_team.html', {'form': form, 'league': league})

@login_required
def team_detail(request,league_id,team_id):
    team = get_object_or_404(Team, id=team_id)
    is_member = team.members.filter(id=request.user.id).exists()
    other_teams_in_league = Team.objects.filter(league=team.league).exclude(id=team_id)
    is_member_of_other_team = other_teams_in_league.filter(members=request.user).exists()
    return render(request, 'leagues/team_detail.html', {'team': team,'is_member': is_member, 'is_member_of_other_team': is_member_of_other_team})

@login_required
def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    league = team.league

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('league_detail', league_id=league.id)
    else:
        form = TeamForm(instance=team)

    return render(request, 'leagues/edit_team.html', {'team': team, 'form': form, 'league': league})

@login_required
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    league_id = team.league.id
    team.delete()
    return redirect('league_detail', league_id=league_id)

@login_required
def leave_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user in team.members.all():
        team.members.remove(request.user)

    return redirect('team_detail', league_id=team.league.id, team_id=team.id)

@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user not in team.members.all():
        team.members.add(request.user)

    return redirect('team_detail', league_id=team.league.id, team_id=team.id)

@login_required
def create_match(request, league_id):
    league = get_object_or_404(League, id=league_id)
    if request.method == 'POST':
        form = MatchForm(request.POST, league=league)
        if form.is_valid():
            match = form.save(commit=False)
            match.league = league
            match.save()
            return redirect('league_detail', league_id=league.id)
    else:
        form = MatchForm(league=league)
    return render(request, 'leagues/create_match.html', {'form': form, 'league': league})

@login_required
def edit_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    league = match.league
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match, league=league)
        if form.is_valid():
            form.save()
            return redirect('league_detail', league_id=league.id)
    else:
        form = MatchForm(instance=match, league=league)
    return render(request, 'leagues/edit_match.html', {'form': form, 'league': league, 'match': match})

@login_required
def delete_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    league_id = match.league.id
    match.delete()
    return redirect('league_detail', league_id=league_id)

@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    return render(request, 'leagues/match_detail.html', {'match': match})

def notifications_list(request):
    notifications = Notification.objects.all()
    return render(request, 'notifications_list.html', {'notifications': notifications})

def clear_all_notifications(request):
    if request.method == 'POST':
        Notification.objects.all().delete()
    return redirect('notifications_list')

def clear_notification(request, notification_id):
    if request.method == 'POST':
        Notification.objects.filter(id=notification_id).delete()
    return redirect('notifications_list')
