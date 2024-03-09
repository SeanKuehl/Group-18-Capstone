from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import AccountLoginForm

class CustomLoginView(LoginView):
    form_class = AccountLoginForm
    template_name = 'login.html'