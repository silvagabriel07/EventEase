from django.test import TestCase
from ..models import User, PhoneNumber
from django.core.files.uploadedfile import SimpleUploadedFile
from eventos.models import Event, Category, Solicitation
from datetime import datetime, timedelta
from django.db.utils import IntegrityError
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError


class TestModelUser(TestCase):
    
    def test_user_image_path(self):
        image = SimpleUploadedFile(
            name='test_img.jpg',
            content=b'\x00\x01\x02\x03',
            content_type='image/jpeg'
        )
        user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
            user_img=image
        )
        self.assertTrue(user.user_img.url.startswith('/user_img/test_img.jpg'))
        default_storage.delete(user.user_img.path)

    def test_create_user_without_user_img_defines_a_default_image(self):
        user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        print(user.user_img.url)
        self.assertEqual(user.user_img, '/user_img/user_img.png')
    
    def test_user_is_minor(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        self.assertTrue(any_user.is_minor())
    
    def test_user_is_not_minor(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=18,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        self.assertFalse(any_user.is_minor())
    
    def test_user_is_a_participant_in_the_event(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        another_user = User.objects.create_user(
            username='another user',
            idade=18,
            email='anotheruser@gmail.com',
            password='senhaqualquer12',
        )
        any_category = Category.objects.create(
            name='Categoria 1'
        )
        event = Event.objects.create(
            title='Titulo 1', 
            description='description etc', 
            organizer=another_user, 
            category_id=1, 
            private=False, 
            free=False,
            start_date_time=datetime.now() + timedelta(days=1), 
            final_date_time=datetime.now() + timedelta(days=2)
        )
        event.participants.add(any_user)
        self.assertTrue(any_user.is_user_participant(event))

    def test_user_is_not_a_participant_in_the_event(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        another_user = User.objects.create_user(
            username='another user',
            idade=18,
            email='anotheruser@gmail.com',
            password='senhaqualquer12',
        )
        any_category = Category.objects.create(
            name='Categoria 1'
        )
        event = Event.objects.create(
            title='Titulo 1', 
            description='description etc', 
            organizer=another_user, 
            category_id=1, 
            private=False, 
            free=False,
            start_date_time=datetime.now() + timedelta(days=1), 
            final_date_time=datetime.now() + timedelta(days=2)
        )
        self.assertFalse(any_user.is_user_participant(event))

    def test_user_has_already_solicitated_for_the_event(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        another_user = User.objects.create_user(
            username='another user',
            idade=18,
            email='anotheruser@gmail.com',
            password='senhaqualquer12',
        )
        any_category = Category.objects.create(
            name='Categoria 1'
        )
        event = Event.objects.create(
            title='Titulo 1', 
            description='description etc', 
            organizer=another_user, 
            category_id=1, 
            private=False, 
            free=False,
            start_date_time=datetime.now() + timedelta(days=1), 
            final_date_time=datetime.now() + timedelta(days=2)
        )
        Solicitation.objects.create(
            user=any_user,
            event=event
        )
        self.assertTrue(any_user.user_already_solicited(event))

    def test_user_has_not_already_solicitated_for_the_event(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        another_user = User.objects.create_user(
            username='another user',
            idade=18,
            email='anotheruser@gmail.com',
            password='senhaqualquer12',
        )
        any_category = Category.objects.create(
            name='Categoria 1'
        )
        event = Event.objects.create(
            title='Titulo 1', 
            description='description etc', 
            organizer=another_user, 
            category_id=1, 
            private=False, 
            free=False,
            start_date_time=datetime.now() + timedelta(days=1), 
            final_date_time=datetime.now() + timedelta(days=2)
        )
        self.assertFalse(any_user.user_already_solicited(event))

    def test_create_user_with_email_that_alredy_exists_fails(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='email@gmail.com',
            password='senhaqualquer12',
        )
        with self.assertRaises(IntegrityError):
            another_user = User.objects.create_user(
                username='another user',
                idade=20,
                email='email@gmail.com',
                password='senhaqualquer12',
            )


class TestManagerCustomUserManager(TestCase):
    
    def test_create_user_without_username(self):
        any_user = User.objects.create_user(
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        self.assertEqual(any_user.username, any_user.email)
    
    def test_create_user_without_password_fails(self):
        with self.assertRaises(ValueError) as context:
            any_user = User.objects.create_user(
                username='test',
                idade=17,
                email='anyuser@gmail.com',
            )
        self.assertEqual(str(context.exception), 'A senha deve ser informada')
            
    def test_create_user_without_email_fails(self):
        with self.assertRaises(TypeError):
            any_user = User.objects.create_user(
                username='test',
                idade=17,
                password='senhaqualquer12'
            )
    
    def test_password_hash_is_created(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        self.assertTrue(any_user.check_password('senhaqualquer12'))
    
    def test_create_user_by_default_as_active(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        self.assertFalse(any_user.is_active)
        
    def test_create_user_by_default_with_is_staff_and_is_superuser_false(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        self.assertFalse(any_user.is_staff)
        self.assertFalse(any_user.is_superuser)
    
    def test_create_superuser_with_is_staff_false_fails(self):
        with self.assertRaises(ValueError) as context:
            any_user = User.objects.create_superuser(
                username='any user',
                idade=17,
                email='anyuser@gmail.com',
                password='senhaqualquer12',
                is_staff=False,
            )
        self.assertEqual(str(context.exception), 'Superuser deve ter is_staff=True.')

    def test_create_superuser_with_is_superuser_false_fails(self):
        with self.assertRaises(ValueError) as context:
            any_user = User.objects.create_superuser(
                username='any user',
                idade=17,
                email='anyuser@gmail.com',
                password='senhaqualquer12',
                is_superuser=False,
            )
        self.assertEqual(str(context.exception), 'Superuser deve ter is_superuser=True.')


class TestModelPhoneNumber(TestCase):
    
    def test_user_cannot_have_more_than_3_phone_numbers(self):
        user = User.objects.create_user(
            username='user',
            idade=19, 
            password='senhaqualquer12',
            email='user@gmail.com'
        )
        for i in range(4):
            phone_number = PhoneNumber(user=user, phone_number=f'+11 12345-123{i}')
            if i == 3:
                with self.assertRaises(ValidationError): 
                    phone_number.save()
            else:
                phone_number.save()
