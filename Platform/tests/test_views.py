from django.test import TestCase
from datetime import datetime, timedelta
from eventos.models import Event, Solicitation, Category
from django.contrib.auth import get_user_model
from django.urls import reverse
# from unittest.mock import patch
# from account_manager.models import PhoneNumber
# from ..forms import ProfileForm
# from django.forms import BaseInlineFormSet

User = get_user_model()

class TestViewExplorarEventos(TestCase):
    
    def setUp(self):
        self.start_date_time = datetime.now() + timedelta(days=1)
        self.final_date_time = datetime.now() + timedelta(days=4)
        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=29, 
            is_active=True
        )
        self.another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='another@gmail.com', 
            idade=18, 
            is_active=True
        )

        Category.objects.create(name='Categoria A')
        self.any_event = Event.objects.create(
            title='Titulo 1', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        self.url = reverse('explorar_eventos')
    
    def test_page_does_not_exist(self):
        response = self.client.get(self.url, data={'page': '99'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('page').number, 1)
    
    def test_page_is_not_an_integer(self):
        response = self.client.get(self.url, data={'page': 'avdewqe3r'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('page').number, 1)   

    def test_select_category_filter_correctly(self):
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='description etc etc', 
            organizer=self.another_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        Category.objects.create(name='Categoria B')
        another_event2 = Event.objects.create(
            title='Titulo 3', 
            description='olá', 
            organizer=self.another_user, 
            category_id=2, 
            private=True, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        response = self.client.get(self.url, data={'select_category': 1})
        self.assertEqual(list(response.context.get('page')), list(Event.objects.filter(category_id=1)))
        self.assertEqual(len(list(response.context.get('page'))), 2)
    
    def test_select_start_date_time_filter_today_correctly(self):
        current_date = datetime.now().date()
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='olá', 
            organizer=self.another_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=current_date, 
            final_date_time=self.final_date_time, 
        )
         
        response = self.client.get(self.url, data={'select_start_date_time': 'today'})
        events = list(response.context.get('page'))
        result = True
        for event in events:
            if not event.start_date_time.date() == current_date:
                result = False
        self.assertTrue(result)
        self.assertEqual(len(events), 1)
        expected_events = Event.objects.filter(id=another_event.id)
        self.assertEqual(events, list(expected_events))

    def test_select_start_date_time_filter_this_month_correctly(self):
        current_date = datetime.now()
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='olá', 
            organizer=self.another_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=current_date + timedelta(days=32), 
            final_date_time=self.final_date_time, 

        )
         
        response = self.client.get(self.url, data={'select_start_date_time': 'this_month'})
        events = list(response.context.get('page'))
        result = True
        for event in events:
            if not event.start_date_time.month == current_date.month:
                result = False
        self.assertTrue(result)
        self.assertEqual(len(events), 1)
        expected_events = Event.objects.filter(id=self.any_event.id)
        self.assertEqual(events, list(expected_events))
        
    def test_select_start_date_time_filter_next_month_correctly(self):
        current_date = datetime.now()
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='olá', 
            organizer=self.another_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=current_date + timedelta(days=31), 
            final_date_time=self.final_date_time, 

        )
         
        response = self.client.get(self.url, data={'select_start_date_time': 'next_month'})
        events = list(response.context.get('page'))
        result = True
        for event in events:
            if not event.start_date_time.month == (current_date + timedelta(days=31)).month:
                result = False
        self.assertTrue(result)
        self.assertEqual(len(events), 1)
        expected_events = Event.objects.filter(id=another_event.id)
        self.assertEqual(events, list(expected_events))

    def test_select_start_date_time_filter_this_year_correctly(self):
        current_date = datetime.now()
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='olá', 
            organizer=self.another_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=datetime(current_date.year+1, 1, 1), 
            final_date_time=self.final_date_time, 
        )
        
        response = self.client.get(self.url, data={'select_start_date_time': 'this_year'})
        events = list(response.context.get('page'))
        result = True
        for event in events:
            if not event.start_date_time.year == current_date.year:
                result = False
        self.assertTrue(result)
        self.assertEqual(len(events), 1)
        expected_events = Event.objects.filter(id=self.any_user.id)
        self.assertEqual(events, list(expected_events))

    def test_select_private_true_filter_correctly(self):
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='description etc etc', 
            organizer=self.another_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        response = self.client.get(self.url, data={'select_private': 'true'})
        expected_events = Event.objects.filter(private=True)
        self.assertEqual(list(response.context.get('page')), list(expected_events))
    
    def test_select_private_false_filter_correctly(self):
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='description etc etc', 
            organizer=self.another_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        response = self.client.get(self.url, data={'select_private': 'false'})
        expected_events = Event.objects.filter(private=False)
        self.assertEqual(list(response.context.get('page')), list(expected_events))
        
    def test_select_free_true_filter_correctly(self):
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='description etc etc', 
            organizer=self.another_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        response = self.client.get(self.url, data={'select_free': 'true'})
        expected_events = Event.objects.filter(free=True)
        self.assertEqual(list(response.context.get('page')), list(expected_events))
    
    def test_select_free_false_filter_correctly(self):
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='description etc etc', 
            organizer=self.another_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        response = self.client.get(self.url, data={'select_free': 'false'})
        expected_events = Event.objects.filter(free=False)
        self.assertEqual(list(response.context.get('page')), list(expected_events))

    def test_select_num_participants_greater_than_filter(self):
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='description etc etc', 
            organizer=self.another_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        for i in range(1, 12):
            user = User.objects.create(username=f'user {i}', idade=20, password='senhaqualquer12', email=f'email{i}@gmail.com')
            self.any_event.participants.add(user)
        
        response = self.client.get(self.url, data={'select_num_participants': 'gt_10'})
        events = list(response.context.get('page'))
        result = True
        for event in events:
            if not event.participants.all().count() >= 10:
                result = False
        self.assertTrue(result)
        self.assertEqual(len(events), 1)
        expected_events = Event.objects.filter(id=self.any_event.id)
        self.assertEqual(events, list(expected_events))
    
    def test_select_num_participants_less_than_filter(self):
        another_event = Event.objects.create(
            title='Titulo 2', 
            description='description etc etc', 
            organizer=self.another_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        for i in range(1, 12):
            user = User.objects.create(username=f'user {i}', idade=20, password='senhaqualquer12', email=f'email{i}@gmail.com')
            self.any_event.participants.add(user)
        
        response = self.client.get(self.url, data={'select_num_participants': 'lt_10'})
        events = list(response.context.get('page'))
        result = True
        for event in events:
            if not event.participants.all().count() <= 10:
                result = False
        self.assertTrue(result)
        self.assertEqual(len(events), 1)
        expected_events = Event.objects.filter(id=another_event.id)
        self.assertEqual(events, list(expected_events))


