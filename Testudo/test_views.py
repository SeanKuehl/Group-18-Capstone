import unittest
from unittest.mock import patch, Mock
from Providers.Steam.views import SteamOAuth2Adapter
from django.http import HttpResponseBadRequest
import requests

class SteamOAuth2AdapterTests(unittest.TestCase):

    @patch('Providers.Steam.views.get_player_summary')
    @patch('Providers.Steam.views.SteamOAuth2Adapter.extract_steam_id')
    @patch('Providers.Steam.views.SteamOAuth2Adapter.get_provider')
    def test_complete_login_success(self, mock_get_provider, mock_extract_steam_id, mock_get_player_summary):
        mock_extract_steam_id.return_value = '123456789'

        mock_get_player_summary.return_value = {'response': {'players': [{'steamid': '123456789'}]}}

        request = Mock()
        app = Mock()
        token = Mock()
        token.extra_data = {'openid': 'http://steamcommunity.com/openid/id/123456789'}

        mock_provider = Mock()
        mock_provider.sociallogin_from_response.return_value = Mock(status_code=200)
        mock_get_provider.return_value = mock_provider

        with patch('Providers.Steam.views.SteamOAuth2Adapter.complete_login', return_value=Mock(status_code=200)) as mock_complete_login:
            adapter_instance = SteamOAuth2Adapter(request) 
            
            response = adapter_instance.complete_login(request, app, token)
            self.assertEqual(response.status_code, 200)
            mock_complete_login.assert_called_once_with(request, app, token)

    @patch('Providers.Steam.views.get_player_summary')
    @patch('Providers.Steam.views.SteamOAuth2Adapter.extract_steam_id')
    @patch('Providers.Steam.views.SteamOAuth2Adapter.get_provider')
    def test_complete_login_failure(self, mock_get_provider, mock_extract_steam_id, mock_get_player_summary):
        mock_extract_steam_id.return_value = '123456789'

        mock_get_player_summary.side_effect = requests.HTTPError("Error fetching profile data")

        request = Mock()
        app = Mock()
        token = Mock()
        token.extra_data = {'openid': 'http://steamcommunity.com/openid/id/123456789'}

        mock_provider = Mock()
        mock_provider.sociallogin_from_response.return_value = Mock(status_code=400)
        mock_get_provider.return_value = mock_provider

        with patch('Providers.Steam.views.SteamOAuth2Adapter.complete_login', return_value=HttpResponseBadRequest("Error fetching profile data")) as mock_complete_login:
            adapter_instance = SteamOAuth2Adapter(request) 
            
            response = adapter_instance.complete_login(request, app, token)
            self.assertEqual(response.status_code, 400)
            mock_complete_login.assert_called_once_with(request, app, token)

if __name__ == '__main__':
    unittest.main()
