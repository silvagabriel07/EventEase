from django.test import TestCase
from ..forms import CustomSignupForm, CustomChangePasswordForm
from ..models import User
from django.core.files.uploadedfile import SimpleUploadedFile

class TestFormCustomSignupForm(TestCase):
    def test_email_already_exists(self):
        user = User.objects.create_user(
            username='another user',
            email='user@gmail.com',
            password='senhaqualquer12',
            idade=88
            )
        
        data = {
            'username': 'user',
            'email': 'user@gmail.com',
            'idade': 17,
            'password1': 'senhaqualquer12',
            'password2': 'senhaqualquer12'
        }
    
        form = CustomSignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='email', errors='Alguém já se registrou com este endereço de e-mail.')
    
    def test_the_email_field_is_missing(self):
        data = {
            'username': 'user',
            'idade': 17,
            'password1': 'senhaqualquer12',
            'password2': 'senhaqualquer12'
        }
        form = CustomSignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='email', errors='Este campo é obrigatório.')

    def test_the_username_field_is_missing(self):
        data = {
            'email': 'user@gmail.com',
            'idade': 17,
            'password1': 'senhaqualquer12',
            'password2': 'senhaqualquer12'
        }
        form = CustomSignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='username', errors='Este campo é obrigatório.')

    def test_the_password1_field_is_missing(self):
        data = {
            'username': 'user',
            'email': 'user@gmail.com',
            'idade': 17,
            'password2': 'senhaqualquer12'
        }
        form = CustomSignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='password1', errors='Este campo é obrigatório.')

    def test_the_password2_field_is_missing(self):
        data = {
            'username': 'user',
            'email': 'user@gmail.com',
            'idade': 17,
            'password1': 'senhaqualquer12'
        }
        form = CustomSignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='password2', errors='Este campo é obrigatório.')

    def test_the_age_field_is_missing(self):
        data = {
            'email': 'user@gmail.com',
            'username': 'user',
            'password1': 'senhaqualquer12',
            'password2': 'senhaqualquer12'
        }
        form = CustomSignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='idade', errors='Este campo é obrigatório.')

    def test_user_without_phone_number_field_sig_up(self):
        user_image = SimpleUploadedFile(
            name='test_user_img.jpg',
            content=b'\x00\x01\x02\x03',
            content_type='image/jpeg'
        )
        data = {
            'username': 'user',
            'email': 'user@gmail.com',
            'idade': 17,
            'password1': 'senhaqualquer12',
            'password2': 'senhaqualquer12',
        }
        form = CustomSignupForm(data=data, files=user_image)
        self.assertTrue(form.is_valid())

    def test_user_without_user_img_field_sig_up(self):
        data = {
            'username': 'user',
            'email': 'user@gmail.com',
            'idade': 17,
            'password1': 'senhaqualquer12',
            'password2': 'senhaqualquer12',
            'phone_number': '+10 10000-1000'
        }
        form = CustomSignupForm(data=data)
        self.assertTrue(form.is_valid())

    def test_user_with_age_less_than_14_cannot_sign_up(self):
        data = {
            'username': 'user',
            'email': 'user@gmail.com',
            'idade': 13,
            'password1': 'senhaqualquer12',
            'password2': 'senhaqualquer12'
        }

        form = CustomSignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='idade', errors='Menores de 14 anos não podem se cadastrar.')
        
