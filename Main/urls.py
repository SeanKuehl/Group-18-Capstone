"""
URL configuration for Testudo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .views import HomePage, SearchResultsView, SignUp, post_index, post_detail, post_tag
from .views import create_account, search_account, user_account, report_post, report_user, MyAccountAndUpdateView
from .views import *

urlpatterns = [
    path('post/', post_index, name="post_index"),
    path("post/<int:pk>/<int:action>/", post_detail, name="post_detail"),
    path("tag/<tag>/", post_tag, name="post_tag"),
    path('', HomePage, name='home'),
    path('signup/', SignUp, name = 'sign_up'),  
    path("search/",SearchResultsView.as_view(), name="search_results"),
    path('create-account/', create_account, name='create_account'),
    path('search-account/', search_account, name='search_account'),
    path('account_page/<int:user_id>/', user_account, name='user_account'),
    path('my_account/<int:pk>', MyAccountAndUpdateView.as_view(), name='my_account'),
    path('report-post/<int:post_id>/', report_post, name='report_post'),
    path('report-user/<int:user_id>/', report_user, name='report_user'),
    path('remove-post/<int:pk>/', remove_post, name='remove_post'),
    path('remove-account/<int:pk>/', remove_account, name='remove_accout'),

]
