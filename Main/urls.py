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

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from Providers.Steam.provider import SteamProvider

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
    path('remove-account/<int:pk>/', remove_account, name='remove_account'),
    path('leagues/', league_list, name='league_list'),
    path('leagues/<int:league_id>/', league_detail, name='league_detail'),
    path('leagues/create/', create_league, name='create_league'),
    path('leagues/<int:league_id>/join/', join_league, name='join_league'),
    path('leagues/<int:league_id>/leave/', leave_league, name='leave_league'),
    path('leagues/<int:league_id>/delete/', delete_league, name='delete_league'),
    path('leagues/<int:league_id>/update/', update_league, name='update_league'),
    path('leagues/<int:league_id>/create_team/', create_team, name='create_team'),
    path('leagues/<int:league_id>/teams/<int:team_id>/', team_detail, name='team_detail'),
    path('leagues/<int:team_id>/edit_team/', edit_team, name='edit_team'),
    path('leagues/<int:team_id>/delete_team/', delete_team, name='delete_team'),
    path('leagues/<int:team_id>/leave_team/', leave_team, name='leave_team'),
    path('leagues/<int:team_id>/join_team/', join_team, name='join_team'),
    path('league/<int:league_id>/create_match/', create_match, name='create_match'),
    path('match/<int:match_id>/edit/', edit_match, name='edit_match'),
    path('match/<int:match_id>/delete/', delete_match, name='delete_match'),
    path('match/<int:match_id>/', match_detail, name='match_detail'),
    path('register-business/',  register_business_number, name='register_business'),
    path('view-discounts/', view_discounts_page, name='discounts'),

    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('notifications/clear_all/', views.clear_all_notifications, name='clear_all_notifications'),
    path('notifications/<int:notification_id>/clear/', views.clear_notification, name='clear_notification'),

    path('search_game/<str:game_name>/', views.search_game_on_steam, name='search_game_on_steam'),
    path('accounts/', include('allauth.urls')),
    
    path('view-events/', ViewEvents, name='events'),
    path('this-event/<int:event_id>', EventDetail, name='event-detail'),
    path('attend-event/<int:event_id>', attend_event, name='attend'),
    path('my_event/<int:pk>', MyEventUpdateView.as_view(), name='my_event'),
]

urlpatterns += default_urlpatterns(SteamProvider)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
