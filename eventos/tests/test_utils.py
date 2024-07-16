from django.contrib import messages
from django.test import TestCase
from eventos.utils import user_is_organizer
from eventos.models import Category, Event, User
from datetime import datetime, timedelta, timezone
from django.urls import reverse

class TestFunctionUserIsOrganizer(TestCase):
    
    def setUp(self) -> None:
        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=17, 
        )
        self.any_user.is_active = True
        self.any_user.save()
        
        self.start_date_time = timezone.now().replace(tzinfo=timezone.utc) + timedelta(days=1) 
        self.final_date_time = self.start_date_time + timedelta(days=20)
        Category.objects.create(name='Categoria A')
        self.any_event = Event.objects.create(
            title='Titulo 1', 
            description='descrition etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
    def test_user_is_organizer_true(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get('/')
        self.assertTrue(user_is_organizer(request=response.wsgi_request, event=self.any_event))
        
    def test_user_is_organizer_false(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=17, 
        )
        Event.objects.create(
            title='Titulo 2', 
            description='descrition etc', 
            organizer=another_user, 
            category_id=1, 
            private=False, 
            free=True,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        another_user.is_active = True
        another_user.save()
        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        response = self.client.get('/')
        self.assertFalse(user_is_organizer(request=response.wsgi_request, event=self.any_event)) 
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), 'Algo deu errado.')
        
    
    def test_user_is_organizer_false_no_message(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=17, 
        )
        Event.objects.create(
            title='Titulo 2', 
            description='descrition etc', 
            organizer=another_user, 
            category_id=1, 
            private=False, 
            free=True,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        another_user.is_active = True
        another_user.save()
        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        response = self.client.get('/')
        self.assertFalse(user_is_organizer(request=response.wsgi_request, event=self.any_event, message=False)) 
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 0)
    