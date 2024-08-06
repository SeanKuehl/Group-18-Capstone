from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.http import urlencode

from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.openid.provider import (
    OpenIDAccount,
    OpenIDProvider,
)


if "allauth.socialaccount.providers.openid" not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        "The steam provider requires 'allauth.socialaccount.providers.openid' to be installed"
    )


class SteamAccount(OpenIDAccount):
    def to_str(self):
        dflt = super(SteamAccount, self).to_str()
        return self.account.extra_data.get("personaname", dflt)

    def get_profile_url(self):
        return self.account.extra_data.get("profileurl")

    def get_avatar_url(self):
        return (
            self.account.extra_data.get("avatarfull")
            or self.account.extra_data.get("avatarmedium")
            or self.account.extra_data.get("avatar")
        )


def extract_steam_id(url):
    prefix = "https://steamcommunity.com/openid/id/"
    if not url.startswith(prefix):
        raise ValueError(url)
    return url[len(prefix) :]


def request_steam_account_summary(api_key, steam_id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
    resp = requests.get(url)
    resp.raise_for_status() 
    return resp.json()


class SteamOpenIDProvider(OpenIDProvider):
    id = "steam"
    name = "Steam"
    account_class = SteamAccount
    uses_apps = True

    def __init__(self, request, app=None):
        if app is None:
            app = get_adapter().get_app(request, self.id)
        super().__init__(request, app=app)

    def get_login_url(self, request, **kwargs):
        url = reverse("steam_login")
        if kwargs:
            url += "?" + urlencode(kwargs)
        return url

    def sociallogin_from_response(self, request, response):
        try:
            response._extra = request_steam_account_summary(settings.STEAM_API_KEY, steam_id)
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e}")
            print("Response content:", e.response.text)
            raise

    def extract_uid(self, response):
        return response._extra["steamid"]

    def extract_extra_data(self, response):
        return response._extra.copy()

    def extract_common_fields(self, response):
        full_name = response._extra.get("realname", "").strip()
        if full_name.count(" ") == 1:
            first_name, last_name = full_name.split()
        else:
            first_name, last_name = full_name, ""

        username = response._extra.get("personaname", "")

        return {
            "username": username or response._extra["steamid"],
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
        }


provider_classes = [SteamOpenIDProvider]
