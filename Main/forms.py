from django import forms
from .models import Post, Comment
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

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'post_community', 'post_body']
        widgets = {
            'post_title': forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            'post_community': forms.TextInput(attrs={"class": "form-control", "placeholder": "Community"}),
            'post_body': forms.Textarea(attrs={"class": "form-control", "placeholder": "Post body here..."}),
        }