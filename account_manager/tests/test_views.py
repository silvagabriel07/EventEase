from django.test import TestCase
from django.urls import reverse
from ..models import User
from unittest.mock import patch

class TestViewAccountInactive(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='user 0',
            email='email@gmail.com',
            password='senhaqualquer12',
            idade=30,
            is_active=True
        )
    
    def test_get_view_account_active_as_a_active_user(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('account_inactive'))
        self.assertRedirects(response, reverse('home'))
        
    def test_get_view_account_inactive_as_a_inactive_user(self):
        response = self.client.get(reverse('account_inactive'))
        self.assertEqual(response.status_code, 200)


class TestViewCustomSignupView(TestCase):
    
    def setUp(self) -> None:
        self.url = reverse('account_signup')
        
    def test_get_signup_return_OK_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_post_signup_with_valid_form(self):
        response = self.client.post(self.url, data={
            'username': 'user',
            'idade': 17,
            'email': 'email@gmail.com',
            'password1': 'senhaqualquer12',
            'password2': 'senhaqualquer12',
        })
        self.assertRedirects(response, reverse('account_inactive'))
        self.assertEqual(User.objects.all().count(), 1)

    @patch('account_manager.views.activateEmail', autospec=True)
    def test_post_signup_with_valid_form_call_activate_Email_function(self, mock_activateEmail):
        response = self.client.post(self.url, data={
            'username': 'user',
            'idade': 17,
            'email': 'email@gmail.com',
            'password1': 'senhaqualquer12',
            'password2': 'senhaqualquer12',
        })
        mock_activateEmail.assert_called_once()

    def test_post_signup_with_invalid_form_redirects_to_signup_with_form_errors(self):
        response = self.client.post(self.url, data={
            'username': 'user',
            'idade': 17,
            'email': 'email@gmail.com',
            'password1': '00000000',
            'password2': 'senhaqualquer12',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context.get('form'))
        self.assertGreaterEqual(len(response.context.get('form').errors), 1)
    

class TestViewCustomLoginView(TestCase):
    
    def setUp(self) -> None:
        self.url = reverse('account_login')
        self.user = User.objects.create_user(
            username='user 0',
            email='email@gmail.com',
            password='senhaqualquer12',
            idade=30,
            is_active=True
        )
    
    def test_get_login_return_OK_status_code(self):
        response =  self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_post_login_inactive_user_with_valid_form(self):
        self.user.is_active = False
        self.user.save()
        
        response = self.client.post(self.url, data={
            'login': 'email@gmail.com',
            'password': 'senhaqualquer12',
        })
        self.assertRedirects(response, reverse('account_inactive'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_post_login_active_user_with_valid_form(self):
        response = self.client.post(self.url, data={
            'login': 'email@gmail.com',
            'password': 'senhaqualquer12',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
    @patch('account_manager.views.activateEmail', autospec=True)
    def test_post_login_with_valid_form_call_activate_Email_function(self, mock_activateEmail):
        self.user.is_active = False
        self.user.save()
        
        response = self.client.post(self.url, data={
            'login': 'email@gmail.com',
            'password': 'senhaqualquer12',
        })
        
        mock_activateEmail.assert_called_once()

    def test_post_login_with_invalid_form_redirects_to_login_with_form_errors(self):
        response = self.client.post(self.url, data={
            'login': 'email@gmail.com',
            'password': 'senhaerrada12',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context.get('form'))
        self.assertGreaterEqual(len(response.context.get('form').errors), 1)

    
