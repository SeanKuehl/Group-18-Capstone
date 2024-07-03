
from django import forms

from .models import *

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from Accounts.models import CustomUser

from Main.models import Post, Comment, League, UserReview, Team, Match, DiscountOffer




class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("account_bio", )   #no need to have the user enter reported count


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={"class": "form-control", "placeholder": "Leave a comment!"})
        }


class DiscountOfferForm(forms.ModelForm):
    class Meta:
        model = DiscountOffer
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={"class": "form-control", "placeholder": "Creat a discount!"})
        }

class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={"class": "form-control", "placeholder": "Leave a review!"})
        }


class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tags"}))

    class Meta:
        model = Post
        fields = ['post_title', 'post_community', 'post_body', 'tags']
        widgets = {
            'post_title': forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            'post_community': forms.TextInput(attrs={"class": "form-control", "placeholder": "Community"}),
            'post_body': forms.Textarea(attrs={"class": "form-control", "placeholder": "Post body here..."}),
        }

        
 class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

    profile_picture = forms.ImageField(required=True)








# The LeagueForm is for creating and updating League instances.
class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'description', 'team_league']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter league name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter league description'}),
        }

# The TeamForm is for creating and updating Team instances.
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name','members']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].widget = forms.CheckboxSelectMultiple()  

# The MatchForm is for creating and updating Match instances.
class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['date', 'team1', 'team2', 'player1', 'player2', 'team1_score', 'team2_score', 'player1_score', 'player2_score']
    
    def __init__(self, *args, **kwargs):
        league = kwargs.pop('league')
        super().__init__(*args, **kwargs)
        if league.team_league:
            self.fields['team1'].queryset = league.teams.all()
            self.fields['team2'].queryset = league.teams.all()
            self.fields['player1'].widget = forms.HiddenInput()
            self.fields['player2'].widget = forms.HiddenInput()
            self.fields['player1_score'].widget = forms.HiddenInput()
            self.fields['player2_score'].widget = forms.HiddenInput()
        else:
            self.fields['player1'].queryset = CustomUser.objects.filter(leagues=league)
            self.fields['player2'].queryset = CustomUser.objects.filter(leagues=league)
            self.fields['team1'].widget = forms.HiddenInput()
            self.fields['team2'].widget = forms.HiddenInput()
            self.fields['team1_score'].widget = forms.HiddenInput()
            self.fields['team2_score'].widget = forms.HiddenInput()

        




class EventForm(forms.ModelForm):
    class Meta:
        model = EventPost
        fields = ['post_title', 'post_location', 'post_date_and_time', 'post_body']
        widgets = {
            'post_title': forms.Textarea(attrs={"class": "form-control", "placeholder": "What is the event"}),
            'post_location': forms.Textarea(attrs={"class": "form-control", "placeholder": "Where the event is happening"}),
            'post_date_and_time': forms.Textarea(attrs={"class": "form-control", "placeholder": "When is the event"}),
            'post_body': forms.Textarea(attrs={"class": "form-control", "placeholder": "Tell people about the event"}),
        }
