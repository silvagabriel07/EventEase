from django.test import TestCase
from ..forms import ProfileForm
from django.core.files.uploadedfile import SimpleUploadedFile

class TestFormProfileForm(TestCase):
    
    def setUp(self) -> None:
        self.any_img = SimpleUploadedFile(
            name='event_banner.png',
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x06bKGD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\tpHYs\x00\x00\x0b\xf8\x00\x00\x0b\xf8\x01\xc7o\xa8d\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00\xc0\xc0\xc0\xf7\xf7\xf7\x00\x00\x00\xfc\x00\x00\x00\x00gAMA\x00\x00\xaf\xc8\x37\x05\x8a\xe9\x00\x00\x00\tpHYs\x00\x00\x0b\xf8\x00\x00\x0b\xf8\x01\xc7o\xa8d\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00\xc0\xc0\xc0\xf7\xf7\xf7\x00\x00\x00\xfc\x00\x00\x00\x00gAMA\x00\x00\xaf\xc8\x37\x05\x8a\xe9\x00\x00\x00\x1aIDATx\xda\xed\xc1\x01\x0d\x00\x00\x08\xc0\xc0\xec\x7fY\x00\x00\x00\x00IEND\xaeB`\x82',
            content_type='image/png'
        )
    
    def test_valid_form(self):
        data = {
            'username': 'user 1',
            'idade': 14,
            'user_img': self.any_img
        }
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_age_less_than_14_invalid_form(self):
        data = {
            'username': 'user 1',
            'idade': 13,
            'user_img': self.any_img
        }
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='idade', errors='Menores de 14 anos não podem se cadastrar.')
    
    def test_missing_idade_field_invalid_form(self):
        data = {
            'username': 'user 1',
            'user_img': self.any_img
        }
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='idade', errors='É necessário informar a idade.')

    def test_missing_username_field_invalid_form(self):
        data = {
            'idade': 13,
            'user_img': self.any_img
        }
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='username', errors='Este campo é obrigatório.')
    
    def test_missing_user_img_valid_form(self):
        data = {
            'username': 'user 1',
            'idade': 14,
        }
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['user_img'], '/user_img/user_img.png')