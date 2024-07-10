import requests
from django.conf import settings

def get_game_details(game_name):
    search_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(search_url)
    if response.status_code == 200:
        apps = response.json().get('applist', {}).get('apps', [])
        for app in apps:
            if app['name'].lower() == game_name.lower():
                game_id = app['appid']
                return game_id
        return None
    else:
        return None