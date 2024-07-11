from django.urls import path, include
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from Providers.Steam.provider import SteamProvider
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Main.urls')),  # Including the URLs from the Main application
]

from Providers.Steam.views import oauth2_login, oauth2_callback

urlpatterns += [
    path('accounts/steam/login/', oauth2_login, name='steam_login'),
    path('accounts/steam/callback/', oauth2_callback, name='steam_callback'),
]
