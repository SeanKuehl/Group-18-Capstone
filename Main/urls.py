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


from .views import *

urlpatterns = [
    path('post/', post_index, name="post_index"),
    path("post/<int:pk>/<int:action>/", post_detail, name="post_detail"),
    path("tag/<tag>/", post_tag, name="post_tag"),
    path('', HomePage, name='home'),
    path('signup/', SignUp, name = 'sign_up'),  
    path("search/",SearchResultsView.as_view(), name="search_results"),
    path('search-account/', search_account, name='search_account'),
    path('account_page/<int:user_id>/', user_account, name='user_account'),
    path('my_account/<int:pk>', MyAccountAndUpdateView.as_view(), name='my_account'),
    path('report-post/<int:post_id>/', report_post, name='report_post'),
    path('report-user/<int:user_id>/', report_user, name='report_user'),
    path('get-existing-tags/', get_existing_tags, name='get_existing_tags'),
    path('remove-post/<int:pk>/', remove_post, name='remove_post'),
    path('remove-account/<int:pk>/', remove_account, name='remove_accout'),
    path('leagues/', league_list, name='league_list'),
    path('leagues/<int:league_id>/', league_detail, name='league_detail'),
    path('leagues/create/', create_league, name='create_league'),
    path('leagues/<int:league_id>/join/', join_league, name='join_league'),
    path('leagues/<int:league_id>/leave/', leave_league, name='leave_league'),
    path('leagues/<int:league_id>/delete/', delete_league, name='delete_league'),
]
