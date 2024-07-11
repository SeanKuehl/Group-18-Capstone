from django.urls import path, include
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from Providers.Steam.provider import SteamProvider

urlpatterns = [
    path('', include('Main.urls')),
]

urlpatterns += default_urlpatterns(SteamProvider)
