from django.test import TestCase
from account_manager.models import User
from django.contrib import messages
from account_manager.utils import need_set_age
from django.urls import reverse
from django.core import mail
from account_manager.utils import activateEmail

class TestUtilsNeedSetAge(TestCase):
        
    def test_need_set_age_with_age(self):
        user_with_age = User.objects.create_user(
            username='user_with_age',
            email='email@gmail.com',
            password='senhaqualquer12',
            idade=20
        )
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('home'))
        
        self.assertFalse(need_set_age(response.wsgi_request, user_with_age))
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 0)

    def test_need_set_age_without_age(self):
        user_without_age = User.objects.create_user(
            username='user_without_age',
            email='email@gmail.com',
            password='senhaqualquer12',
        )
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('home'))
        
        self.assertTrue(need_set_age(response.wsgi_request, user_without_age))
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)


class TestUtilsActivateEmail(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='user',
            email='email@gmail.com',
            password='senhaqualquer12',
            idade=20
        )
        
    def test_activate_email_is_sent(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get('home')
        activateEmail(response.wsgi_request, self.user, self.user.email)
        
        self.assertEqual(len(mail.outbox), 1)
    
    def test_activate_email_link_with_token_sent_is_valid(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('home'))
        activateEmail(response.wsgi_request, self.user, self.user.email)        
        email = mail.outbox[0].body
        if 'example.com' in email:
            email = email.replace('example.com', 'http://127.0.0.1:8000')
        url = email.split()[-1]
        response = self.client.get(url)
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)