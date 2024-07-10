from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.openid.provider import OpenIDProvider

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

provider_classes = [SteamProvider]