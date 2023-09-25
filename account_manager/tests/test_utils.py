from django.test import TestCase
from ..models import User
from django.contrib import messages
from ..utils import need_set_age
from django.urls import reverse

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

