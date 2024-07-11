from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.openid.provider import OpenIDProvider
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from Providers.Steam.views import SteamOAuth2LoginView, SteamOAuth2CallbackView

class SteamAccount(ProviderAccount):
    def to_str(self):
        return self.account.extra_data.get('personaname', super().to_str())

class SteamProvider(OpenIDProvider):
    id = 'steam'
    name = 'Steam'
    account_class = SteamAccount

    def extract_uid(self, data):
        return str(data['sub'])

    def extract_extra_data(self, data):
        return data

    def get_login_view(self):
        return SteamOAuth2LoginView

    def get_callback_view(self):
        return SteamOAuth2CallbackView

provider_classes = [SteamProvider]
