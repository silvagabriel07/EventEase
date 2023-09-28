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


