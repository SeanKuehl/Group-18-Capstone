from django.test import TestCase, Client
from django.urls import reverse
from Main.models import Account

class LoginTests(TestCase):

    # Create a test user for testing, follows the Account model in Main/models.py
    def setUp(self):
        self.client = Client()
        self.user = Account(username='test', password='password')
        self.user.save()

    # Ensure that page renders
    def test_login_page_render(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')  

    # Test valid user can log in 
    def test_login(self):
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': 'test', 'password': 'password'})
        self.assertEqual(response.status_code, 200)

    # Test invalid log in credentials
    def test_invalid_login(self):
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': 'invalid', 'password': 'invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)