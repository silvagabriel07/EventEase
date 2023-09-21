from django.db.models.signals import post_save, m2m_changed
from notifications.models import Notification
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.test import override_settings
from datetime import datetime, timedelta
from eventos.models import Event, Solicitation, Category
from ..signals import send_solicitation_notification, send_participant_notification

start_of_url = 'http://127.0.0.1:8000'
User = get_user_model()

class TestSignalsSendSolicitationNotification(TestCase):
    def setUp(self):
        start_date_time = datetime.now() + timedelta(days=2)
        final_date_time = datetime.now() + timedelta(days=4)
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
            start_date_time=start_date_time, 
            final_date_time=final_date_time, 
        )

    @override_settings(USE_TZ=False)
    def test_send_notification_to_solicitation_created_creates_a_notification_correctly(self):
        solicitation = Solicitation.objects.create(
            user=self.another_user,
            event=self.any_event,  
        )

        expected_url =  reverse('ver_mais', args=[self.any_event.id])
        self.assertEqual(self.any_user.notifications.all().count(), 1)
        self.assertEqual(self.any_user.notifications.first().verb, f'Solicitou participação para o evento <a class="link" href="{start_of_url+expected_url}">'+self.any_event.title+'</a>.')
        self.assertEqual(Notification.objects.all().count(), 1)

    @override_settings(USE_TZ=False)
    def test_send_notification_to_solicitation_created_creates_a_notification_correctly(self):
        self.any_event.banned_users.add(self.another_user)
        solicitation = Solicitation.objects.create(
            user=self.another_user,
            event=self.any_event,
        )

        expected_url =  reverse('ver_mais', args=[self.any_event.id])
        self.assertEqual(self.any_user.notifications.all().count(), 1)
        self.assertEqual(self.any_user.notifications.first().verb, f'O usuário {self.another_user.username}, que <u>havia sido banido</u> do evento <a class="link" href="{start_of_url+expected_url}">'+self.any_event.title+'</a>, solicitou participação.')
        self.assertEqual(Notification.objects.all().count(), 1)

    @override_settings(USE_TZ=False)
    def test_send_notification_to_solicitation_accepted_creates_a_notification_correctly(self):
        solicitation = Solicitation.objects.create(
            user=self.another_user,
            event=self.any_event,  
        )
        solicitation.status = 'a'
        solicitation.save()
        expected_url = reverse('ver_mais', args=[self.any_event.id])
        
        self.assertEqual(self.another_user.notifications.all().count(), 1)
        self.assertEqual(self.another_user.notifications.first().verb, f'Sua solicitação de participação para o evento <a class="link" href="{start_of_url+expected_url}">'+self.any_event.title+'</a> foi <b>aceita</b>. Agora você participa do evento 😊')
        self.assertEqual(Notification.objects.all().count(), 2)

    @override_settings(USE_TZ=False)
    def test_send_notification_to_solicitation_rejected_creates_a_notification_correctly(self):
        solicitation = Solicitation.objects.create(
            user=self.another_user,
            event=self.any_event,  
        )
        solicitation.status = 'r'
        solicitation.save()
        expected_url = reverse('ver_mais', args=[self.any_event.id])
        
        self.assertEqual(self.another_user.notifications.all().count(), 1)
        self.assertEqual(self.another_user.notifications.first().verb, f'Sua solicitação de participação para o evento <a class="link" href="{start_of_url+expected_url}">'+self.any_event.title+'</a> foi <b>rejeitada</b>.')
        self.assertEqual(Notification.objects.all().count(), 2)
    
    
class TestSignalsSendParticipantNotification(TestCase):
    def setUp(self):
        start_date_time = datetime.now() + timedelta(days=2)
        final_date_time = datetime.now() + timedelta(days=4)
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
            start_date_time=start_date_time, 
            final_date_time=final_date_time, 
        )
    
    @override_settings(USE_TZ=False)
    def test_send_notification_to_add_participant_creates_a_notification_correctly(self):
        self.any_event.participants.add(self.another_user)
        expected_url = reverse('ver_mais', args=[self.any_event.id])
        
        self.assertEqual(self.any_user.notifications.all().count(), 1)
        self.assertEqual(self.any_user.notifications.first().verb, f'O usuário <u>{self.another_user.username} entrou</u> no seu evento <a class="link" href="{start_of_url+expected_url}">'+self.any_event.title+'</a>.')
        self.assertEqual(Notification.objects.all().count(), 1)

    @override_settings(USE_TZ=False)
    def test_send_notification_to_remove_participant_creates_a_notification_correctly(self):
        self.any_event.participants.add(self.another_user)
        self.any_event.participants.remove(self.another_user)
        expected_url = reverse('ver_mais', args=[self.any_event.id])
        
        self.assertEqual(self.another_user.notifications.all().count(), 1)
        self.assertEqual(self.another_user.notifications.first().verb, f'<u>Você foi removido</u> do evento <a class="link" href="{start_of_url+expected_url}">'+self.any_event.title+'</a>.')
        self.assertEqual(Notification.objects.all().count(), 2)




