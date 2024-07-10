from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import SteamProvider

urlpatterns = default_urlpatterns(SteamProvider)