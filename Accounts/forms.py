from django import forms
from django.contrib.auth.forms import AuthenticationForm

class AccountLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']