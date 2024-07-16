from django.test import TestCase
from datetime import datetime, timedelta
from django.utils import timezone
from eventos.models import Event, Solicitation, Category
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch
from account_manager.models import PhoneNumber
from Platform.forms import ProfileForm
from django.forms import BaseInlineFormSet
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class TestViewExplorarEventos(TestCase):
    
    def setUp(self):
        self.start_date_time = timezone.now() + timedelta(days=1)
        self.final_date_time = timezone.now() + timedelta(days=4)
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
        current_date = timezone.now().date()
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
        current_date = timezone.now()
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
        current_date = timezone.now()
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
        current_date = timezone.now()
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


class TestViewPerfil(TestCase):
    
    def setUp(self) -> None:
        self.url = reverse('perfil')

        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=29, 
            is_active=True
        )        
        self.client.login(password='senhaqualquer12', email='email@gmail.com')

    # GET REQUEST    
    def test_get_request_renders_what_is_expected(self):
        self.client.login(password='senhaqualquer12', email='email@gmail.com')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ProfileForm)
        self.assertIsInstance(response.context['form_filho'], BaseInlineFormSet)
  
    @patch('Platform.views.forms.inlineformset_factory', spec=True)
    def test_number_of_phone_numbers_input_correctly(self, mock_form_factory):
        for n in range(0, 4):
            if n != 0:
                phone_number = PhoneNumber(user=self.any_user, phone_number=f'+00 00000-000{n}')
                phone_number.save()
            response = self.client.get(self.url)
            amount_phonenumber_inputs = mock_form_factory.call_args[1]['extra']
            self.assertEqual(amount_phonenumber_inputs, 3 - n)

    # POST REQUEST
    # Because I am testing a view, I will not focus on testing the form itself,
    # but rather on the view's behavior with the forms.
    def test_POST_update_only_username_valid(self):
        form_data = {
            'username': 'newusername',
            'idade': self.any_user.idade,
            'phonenumber_set-TOTAL_FORMS': '3', # number of forms submitted to be rendered
            'phonenumber_set-INITIAL_FORMS': '0', # amount of forms linked to user instance (in this case)
            'phonenumber_set-MIN_NUM_FORMS': '3',
            'phonenumber_set-MAX_NUM_FORMS': '3',
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após POST bem-sucedido

        self.any_user.refresh_from_db()
        self.assertEqual(self.any_user.username, 'newusername')
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Alterações salvas.')
    
    def test_POST_adding_a_new_phone_number_valid(self):
        form_data = {
            'username': self.any_user.username,
            'idade': self.any_user.idade,
            'phonenumber_set-TOTAL_FORMS': '3',
            'phonenumber_set-INITIAL_FORMS': '0',
            'phonenumber_set-MIN_NUM_FORMS': '3',
            'phonenumber_set-MAX_NUM_FORMS': '3',
            
            'phonenumber_set-0-phone_number': '+11 11111-1111',
        }       
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)  
        self.any_user.refresh_from_db()
        self.assertTrue(self.any_user.phonenumber_set.all().exists())
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Alterações salvas.')

           
    def test_POST_update_only_phone_number_valid(self):
        phone_number = PhoneNumber(user=self.any_user, phone_number='+00 00000-0000')
        phone_number.save()
    
        form_data = {
            'username': self.any_user.username,
            'idade': self.any_user.idade,
            'phonenumber_set-TOTAL_FORMS': '3',
            'phonenumber_set-INITIAL_FORMS': '1',
            'phonenumber_set-MIN_NUM_FORMS': '3',
            'phonenumber_set-MAX_NUM_FORMS': '3',
            
            'phonenumber_set-0-user': self.any_user.id,
            'phonenumber_set-0-id': phone_number.id,
            'phonenumber_set-0-phone_number': '+11 11111-1111',
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302) 
        
        self.any_user.refresh_from_db()
        self.assertEqual(PhoneNumber.objects.get(id=1).phone_number, '+11 11111-1111')
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Alterações salvas.')


    def test_POST_invalid_phone_number(self):
        form_data = {
            'username': self.any_user.username,
            'idade': self.any_user.idade,
            'phonenumber_set-TOTAL_FORMS': '1',
            'phonenumber_set-INITIAL_FORMS': '0',
            'phonenumber_set-MIN_NUM_FORMS': '',
            'phonenumber_set-MAX_NUM_FORMS': '',
            
            'phonenumber_set-0-phone_number': '010 93099-3900',
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(self.any_user.phonenumber_set.all().exists())


class TestViewVerPerfil(TestCase):
    
    def setUp(self) -> None:
        self.start_date_time = timezone.now() + timedelta(days=1)
        self.final_date_time = timezone.now() + timedelta(days=4)
        Category.objects.create(name='Categoria A')

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
    
    def test_ver_perfil_view(self):
        for i in range(3):
            organizer = self.any_user
            if i == 2:
                organizer = self.another_user
                
            Event.objects.create(
                title=f'Titulo {i}', 
                description=f'description etc {i}', 
                organizer=organizer, 
                category_id=1, 
                private=False, 
                free=False,             
                start_date_time=self.start_date_time, 
                final_date_time=self.final_date_time, 
            )
        other_event = Event.objects.get(id=3)
        other_event.participants.add(self.any_user)
        
        response = self.client.get(reverse('ver_perfil', args=[self.any_user.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('qtd_events_organizing'), 2)
        self.assertEqual(response.context.get('qtd_event_participanting'), 1)
        

    def test_user_does_not_exist(self):
        response = self.client.get(reverse('ver_perfil', args=[10]))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Usuário não existe.')
        self.assertRedirects(response, reverse('home'))
        
    def test_view_render_correctly_template(self):
        response = self.client.get(reverse('ver_perfil', args=[self.any_user.id]))
        self.assertTemplateUsed(response, 'ver_perfil.html')

        
class TestViewVerEventosParticipando(TestCase):
    
    def setUp(self) -> None:
        self.start_date_time = timezone.now() + timedelta(days=1)
        self.final_date_time = timezone.now() + timedelta(days=4)
        Category.objects.create(name='Categoria A')

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
    
    def test_ver_eventos_participando_view(self):
        for i in range(3):                
            event = Event.objects.create(
                title=f'Titulo {i}', 
                description=f'description etc {i}', 
                organizer=self.any_user, 
                category_id=1, 
                private=False, 
                free=False,             
                start_date_time=self.start_date_time, 
                final_date_time=self.final_date_time, 
            )        
            event.participants.add(self.another_user)
        response = self.client.get(reverse('ver_eventos_participando', args=[self.another_user.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('events_participanting').count(), 3)

    def test_user_does_not_exist(self):
        response = self.client.get(reverse('ver_eventos_participando', args=[10]))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Usuário não existe.')
        self.assertRedirects(response, reverse('home'))

    def test_view_render_correctly_template(self):
        response = self.client.get(reverse('ver_eventos_participando', args=[self.any_user.id]))
        self.assertTemplateUsed(response, 'ver_eventos_participando.html')



class TestViewVerEventosOrganizando(TestCase):
    
    def setUp(self) -> None:
        self.start_date_time = timezone.now() + timedelta(days=1)
        self.final_date_time = timezone.now() + timedelta(days=4)
        Category.objects.create(name='Categoria A')

        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=29, 
            is_active=True
        )

    def test_ver_eventos_organizando_view(self):
        for i in range(3):                
            event = Event.objects.create(
                title=f'Titulo {i}', 
                description=f'description etc {i}', 
                organizer=self.any_user, 
                category_id=1, 
                private=False, 
                free=False,             
                start_date_time=self.start_date_time, 
                final_date_time=self.final_date_time, 
            )       
            
        response = self.client.get(reverse('ver_eventos_organizando', args=[self.any_user.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('events_organizing').count(), 3)

    def test_user_does_not_exist(self):
        response = self.client.get(reverse('ver_eventos_organizando', args=[10]))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Usuário não existe.')
        self.assertRedirects(response, reverse('home'))

    def test_view_render_correctly_template(self):
        response = self.client.get(reverse('ver_eventos_organizando', args=[self.any_user.id]))
        self.assertTemplateUsed(response, 'ver_eventos_organizando.html')


    