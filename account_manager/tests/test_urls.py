from django.test import TestCase
from django.urls import reverse
from account_manager.models import User
from django.db.utils import IntegrityError
from unittest.mock import patch
from django.core.exceptions import ValidationError

class TestUrlsDjangoOAuth(TestCase):
    
    def setUp(self) -> None:
        self.any_user = User.objects.create_user(
            username='user',
            email='anyuser@gmail.com',
            password='senhaqualquer12',
            idade=16,
            is_active='True'
        )
    
    # signup
    def test_get_signup_url_OK(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_signup_url_template_OK(self):
        response = self.client.get(reverse('account_signup'))
        self.assertContains(response, 'template-Eventease')
    
    # login
    def test_get_login_url_OK(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_url_template_OK(self):
        response = self.client.get(reverse('account_login'))
        self.assertContains(response, 'template-Eventease')
        
    # set_password
    def test_get_set_password_url_is_not_OK_when_user_signup_normally(self):
        with self.assertRaises(ValidationError):
            user = User.objects.create_user(
                username='user',
                email='email@gmail.com',
                idade=16,
                is_active='True'
            )

        user = User.objects.create_user(
            username='user',
            email='email@gmail.com',
            idade=16,
            password='senhaqualquer12',
            is_active='True'
        )

        user.password = ''
        user.save()
        
        self.client.force_login(user)
        
        response = self.client.get(reverse('account_set_password'))
        self.assertEqual(response.status_code, 302)
        
        user.password = None
        with self.assertRaises(IntegrityError):
            user.save() 
    
    @patch('account_manager.models.password_validate')
    def test_get_set_password_url_is_OK_when_user_has_not_password(self, mock_password_validate):
        mock_password_validate.return_value = None
        user = User.objects.create_user(
            username='user',
            email='email@gmail.com',
            idade=16,
            is_active='True'
        )
        
        self.client.force_login(user)
        
        response = self.client.get(reverse('account_set_password'))
        self.assertEqual(response.status_code, 200)

    @patch('account_manager.models.password_validate')
    def test_get_set_password_tamplate_is_OK_when_user_has_not_password(self, mock_password_validate):
        mock_password_validate.return_value = None
        user = User.objects.create_user(
            username='user',
            email='email@gmail.com',
            idade=16,
            is_active='True'
        )
        
        self.client.force_login(user)
        
        response = self.client.get(reverse('account_set_password'))
        self.assertContains(response, 'template-Eventease')

    # change_password
    def test_get_change_password_url_OK(self):
        self.client.login(email='anyuser@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('account_change_password'))
        self.assertEqual(response.status_code, 200)
    
    def test_change_password_url_template_OK(self):
        self.client.login(email='anyuser@gmail.com', password='senhaqualquer12')

        response = self.client.get(reverse('account_change_password'))
        self.assertContains(response, 'template-Eventease')
    
    # reset_password
    def test_get_reset_password_url_OK(self):
        self.client.login(email='anyuser@gmail.com', password='senhaqualquer12')

        response = self.client.get(reverse('account_reset_password'))
        self.assertEqual(response.status_code, 200)
        
    def test_reset_passoword_url_template_OK(self):
        self.client.login(email='anyuser@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('account_reset_password'))
        self.assertContains(response, 'template-Eventease')
    
    # reset_password_done
    def test_get_reset_password_done_url_OK(self):
        self.client.login(email='anyuser@gmail.com', password='senhaqualquer12')

        response = self.client.get(reverse('account_reset_password_done'))
        self.assertEqual(response.status_code, 200)
        
    def test_reset_password_done_url_template_OK(self):
        self.client.login(email='anyuser@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('account_reset_password_done'))
        self.assertContains(response, 'template-Eventease')
    
    # reset_password_from_key        
    def test_reset_password_from_key_url_template_and_status_code_OK(self):
        response = self.client.get(reverse('account_reset_password_from_key', args=['u2', 'tokenFAKEuacvbuwbnvijni2wnefcn']), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'template-Eventease')
    
    def test_reset_password_from_key_url_with_invalid_token(self):
        response = self.client.get(reverse('account_reset_password_from_key', args=['u2', 'tokenFAKEuacvbuwbnvijni2wnefcn']), follow=True)
        self.assertContains(response, 'token-invalidado')
    
    # account_reset_password_from_key_done
    def test_get_account_reset_password_from_key_done_url_OK(self):
        self.client.login(email='anyuser@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('account_reset_password_from_key_done'))
        self.assertEqual(response.status_code, 200)
    
    def test_account_reset_password_from_key_done_url_template_OK(self):
        self.client.login(email='anyuser@gmail.com', password='senhaqualquer12')

        response = self.client.get(reverse('account_reset_password_from_key_done'))
        self.assertContains(response, 'template-Eventease')

    

    

