from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView

class SteamOAuth2Adapter:
    provider_id = SteamProvider.id
    authorize_url = "https://steamcommunity.com/openid/login"
    access_token_url = "https://steamcommunity.com/openid/login"
    profile_url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"


oauth2_login = OAuth2LoginView.adapter_view(SteamOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SteamOAuth2Adapter)
