from django import forms
from .models import Post, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={"class": "form-control", "placeholder": "Leave a comment!"})
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