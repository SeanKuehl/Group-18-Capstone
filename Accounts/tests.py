from django.test import TestCase, Client
from django.urls import reverse
from Main.models import Account
from django.contrib.auth.models import User
from django.conf import settings

class LoginTests(TestCase):

    # Create a test user for testing, follows the Account model in Main/models.py
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test', 
            email='test@example.com', 
            password='password')
        self.account = Account.objects.create(
            user_owner=self.user,
            username='test',
            email='test@example.com',
            account_name='Test Account',
            account_bio='hello world'
        )
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
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL)

    # Test invalid log in credentials
    def test_invalid_login(self):
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': 'invalid', 'password': 'invalid'})
        self.assertNotIn('_auth_user_id', self.client.session)