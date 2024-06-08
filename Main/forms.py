from django import forms

from .models import *

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from Accounts.models import CustomUser




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

# The LeagueForm is for creating and updating League instances.
class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter league name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter league description'}),
        }



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