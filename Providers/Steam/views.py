from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView

class SteamOAuth2LoginView(OAuth2LoginView):
    view_name = "steam_login"

class SteamOAuth2CallbackView(OAuth2CallbackView):
    view_name = "steam_callback"
