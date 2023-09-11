from django.test import TestCase
from ..models import Event, Category, User, Solicitation
from datetime import datetime, timedelta, timezone
from django.db.utils import IntegrityError

class TestModelEvent(TestCase):
    
    def setUp(self) -> None:
        self.any_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=19, 
        )
        
        organizer = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=17, 
        )
        
        any_category = Category.objects.create(
            name='Categoria 1'
            )
        
        start_date_time = datetime.now().replace(tzinfo=timezone.utc) + timedelta(days=1) 
        final_date_time = start_date_time + timedelta(days=20)

        self.any_event = Event.objects.create(
            title='Titulo 1', 
            description='descrition etc', 
            organizer=organizer, 
            category=self.any_category, 
            private=False, 
            free=False,             
            start_date_time=start_date_time, 
            final_date_time=final_date_time, 
        )
    
    # ban_user method test
    def test_method_ban_user_success(self):
        user = self.any_user
        event = self.any_event
        self.assertEqual(event.banned_users.count(), 0)
        self.assertTrue(event.ban_user(user_id=user.id))
        self.assertEqual(event.banned_users.count(), 1)
        
    def test_method_ban_user_does_not_exist(self):
        event = self.any_event
        self.assertEqual(event.banned_users.count(), 0)
        self.assertFalse(event.ban_user(user_id=100))
        self.assertEqual(event.banned_users.count(), 0)
    
    
    # unban_user method test
    def test_method_unban_user_success(self):
        user = self.any_user
        event = self.any_event
        event.banned_users.add(user)
        self.assertEqual(event.banned_users.count(), 1)
        self.assertTrue(event.unban_user(user_id=user.id))
        self.assertEqual(event.banned_users.count(), 0)

    def test_method_unban_user_does_not_exist(self):
        user = User.objects.get(username='user 2')
        event = self.any_event
        event.banned_users.add(user)
        self.assertEqual(event.banned_users.count(), 1)
        self.assertFalse(event.unban_user(user_id=10))
        self.assertEqual(event.banned_users.count(), 1)
    
    
    # user_is_banned method test
    def test_user_is_banned_success(self):
        user = self.any_user
        event = self.any_event
        event.ban_user(user_id=user.id)
        self.assertTrue(event.is_banned_user(user.id))
    
    def test_user_is_banned_does_not_exist(self):
        event = self.any_event
        self.assertFalse(event.is_banned_user(999))


    # has_passed method test
    def test_has_passed_True(self):
        event_passed = Event.objects.create(
            title='Titulo 1', 
            description='descrition etc', 
            organizer=self.any_user, 
            category=self.any_category, 
            private=False, 
            free=False,             
            start_date_time=datetime.now().replace(tzinfo=timezone.utc) - timedelta(days=2), 
            final_date_time=datetime.now().replace(tzinfo=timezone.utc) - timedelta(days=1), 
        )
        self.assertTrue(event_passed.has_passed())
        
    def test_has_passed_False(self):
        self.assertFalse(self.any_event.has_passed())


    # accept_user method test
    def test_accept_user_success(self):
        solicitation = Solicitation.objects.create(user=self.any_user, event=self.any_event)
        self.assertEqual(self.any_event.qtd_solicitations, 1)
        self.assertEqual(self.any_event.qtd_participants, 0)
        self.assertTrue(self.any_event.accept_user(self.any_user.id))
        self.assertEqual(self.any_event.qtd_solicitations, 0)
        self.assertEqual(self.any_event.qtd_participants, 1)
        solicitation = self.any_event.solicitation_set.get(id=solicitation.id)
        self.assertEqual(solicitation.status, 'a')
    
    def test_accept_user_does_not_exist(self):
        self.assertFalse(self.any_event.accept_user(999))
            
    
    # reject_user method test
    def test_rejept_user_success(self):
        solicitation = Solicitation.objects.create(user=self.any_user, event=self.any_event)
        self.assertEqual(self.any_event.qtd_solicitations, 1)
        self.assertEqual(self.any_event.qtd_participants, 0)
        self.assertTrue(self.any_event.reject_user(self.any_user.id))
        self.assertEqual(self.any_event.qtd_solicitations, 0)
        self.assertEqual(self.any_event.qtd_participants, 0)
        solicitation = self.any_event.solicitation_set.get(id=solicitation.id)
        self.assertEqual(solicitation.status, 'r')

    def test_accept_user_does_not_exist(self):
        self.assertFalse(self.any_event.reject_user(999))


    # remove_user method test
    def test_remove_user_success(self):
        self.any_event.participants.add(self.any_user)
        self.assertEqual(self.any_event.qtd_participants, 1)
        self.assertTrue(self.any_event.remove_user(self.any_user.id))
        self.assertEqual(self.any_event.qtd_participants, 0)
    
    

class TestModelSolicitation(TestCase):
    
    def setUp(self) -> None:
        self.any_user = User.objects.create(
            username='user qualquer',
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=19, 
        )
        organizer = User.objects.create(
            username='user qualquer',
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=19, 
        )
        any_category = Category.objects.create(
            name='Categoria 1'
            )
        
        start_date_time = datetime.now().replace(tzinfo=timezone.utc) + timedelta(days=1) 
        final_date_time = start_date_time + timedelta(days=20)

        self.any_event = Event.objects.create(
            title='Titulo 1', 
            description='descrition etc', 
            organizer=organizer, 
            category=any_category, 
            private=False, 
            free=False,             
            start_date_time=start_date_time, 
            final_date_time=final_date_time, 
        )
    
    def test_user_and_event_is_unique_toguether(self):
        Solicitation.objects.create(user=self.any_user, event=self.any_event)
        with self.assertRaises(IntegrityError):
            Solicitation.objects.create(user=self.any_user, event=self.any_event)

