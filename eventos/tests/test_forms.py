from django.test import TestCase
from eventos.forms import EventForm, Category, Event
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta, timezone
import os

# PRECISO FAZER MUITO MAIS TESTES PARA ESSE FORM
# PRECISO COBRIR TODAS AS POSSIVILIDADES DE ERRO COM ESSE FORM.
class TestFormEventForm(TestCase):
    
    def setUp(self) -> None:
        # Crie um arquivo temporário simulado
        self.start_date_time = (timezone.now() + timedelta(days=2)).strftime('%d/%m/%Y')
        self.final_date_time = (timezone.now() + timedelta(days=4)).strftime('%d/%m/%Y')

        self.uploaded_file = SimpleUploadedFile(
            name='event_banner.png',
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x06bKGD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\tpHYs\x00\x00\x0b\xf8\x00\x00\x0b\xf8\x01\xc7o\xa8d\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00\xc0\xc0\xc0\xf7\xf7\xf7\x00\x00\x00\xfc\x00\x00\x00\x00gAMA\x00\x00\xaf\xc8\x37\x05\x8a\xe9\x00\x00\x00\tpHYs\x00\x00\x0b\xf8\x00\x00\x0b\xf8\x01\xc7o\xa8d\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00\xc0\xc0\xc0\xf7\xf7\xf7\x00\x00\x00\xfc\x00\x00\x00\x00gAMA\x00\x00\xaf\xc8\x37\x05\x8a\xe9\x00\x00\x00\x1aIDATx\xda\xed\xc1\x01\x0d\x00\x00\x08\xc0\xc0\xec\x7fY\x00\x00\x00\x00IEND\xaeB`\x82',
            content_type='image/png'
        )
        self.category = Category.objects.create(name='Categoria Qualquer') 
                
    def test_create_event_successfully_without_event_banner(self):
        data = {
            'title': 'Título Qualquer',
            'description': 'Decrição qualquer',
            'category': self.category,
            'start_date_time': self.start_date_time+' 20:20',
            'final_date_time': self.final_date_time+' 20:20',
        }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['event_banner'], '/event_banners/default_event_banner.png')
    
    def test_valid_event_form_succesful_with_banner(self):
        data = {
            'title': 'Título Qualquer',
            'description': 'Descrição qualquer',
            'category': self.category,  
            'start_date_time': self.start_date_time+' 20:20',
            'final_date_time': self.final_date_time+' 20:20',
        }

        form = EventForm(data, {'event_banner': self.uploaded_file})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['event_banner'], self.uploaded_file)    
    
    def test_DateTimeField_invalid_formats_1(self):
        data = {
            'title': 'Título Qualquer',
            'description': 'Descrição qualquer',
            'category': self.category,  
            'start_date_time': '10-09-2023 20:20',
            'final_date_time': '10-09-2023 20:20'
        }

        form = EventForm(data, {'event_banner': self.uploaded_file})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors['start_date_time']), 1)
        self.assertEqual(len(form.errors['final_date_time']), 1)
        
    def test_DateTimeField_invalid_formats_2(self):
        data = {
            'title': 'Título Qualquer',
            'description': 'Descrição qualquer',
            'category': self.category,  
            'start_date_time': '2023/09/20 20:10',
            'final_date_time': '2023/10/01 19:05'
        }

        form = EventForm(data, {'event_banner': self.uploaded_file})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors['start_date_time']), 1)
        self.assertEqual(len(form.errors['final_date_time']), 1)
        
    def test_DateTimeField_invalid_formats_3(self):
        data = {
            'title': 'Título Qualquer',
            'description': 'Descrição qualquer',
            'category': self.category,  
            'start_date_time': '16/10/2023 20-10',
            'final_date_time': '16/10/2023 20-10'
        }

        form = EventForm(data, {'event_banner': self.uploaded_file})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors['start_date_time']), 1)
        self.assertEqual(len(form.errors['final_date_time']), 1)

    def test_DateTimeField_start_data_time_after_final_date_time(self):
        start_date_time = final_date_time = (timezone.now() + timedelta(days=1)).strftime('%d/%m/%Y')

        data = {
            'title': 'Título Qualquer',
            'description': 'Descrição qualquer',
            'category': self.category,  
            'start_date_time': start_date_time+' 20:20',
            'final_date_time': final_date_time+' 20:00',
        }

        form = EventForm(data, {'event_banner': self.uploaded_file})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Data inicial não pode ser após a data final do evento.')

    def test_DateTimeField_has_passed(self):
        start_date_time = (timezone.now() - timedelta(days=2)).strftime('%d/%m/%Y')
        final_date_time = (timezone.now() - timedelta(days=1)).strftime('%d/%m/%Y')
        data = {
            'title': 'Título Qualquer',
            'description': 'Descrição qualquer',
            'category': self.category,  
            'start_date_time': start_date_time+' 20:00',
            'final_date_time': final_date_time+' 21:09',
        }
        form = EventForm(data, {'event_banner': self.uploaded_file})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Data informada já passou.')

    def test_start_date_time_and_final_date_time_is_equal(self):
        start_date_time = final_date_time = (timezone.now() + timedelta(days=1)).strftime('%d/%m/%Y')
        data = {
            'title': 'Título Qualquer',
            'description': 'Descrição qualquer',
            'category': self.category,  
            'start_date_time': start_date_time+' 20:00',
            'final_date_time': final_date_time+' 20:00',
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'O evento termina e começa no mesmo momento.')

    def test_missing_title_field(self):
        data = {
            'title': '',
            'description': 'Descrição qualquer',
            'category': self.category,  
            'start_date_time': self.start_date_time+' 20:20',
            'final_date_time': self.final_date_time+' 20:20'
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='title', errors='Este campo é obrigatório.')

    def test_missing_description_field(self):
        data = {
            'title': 'Título 1',
            'description': '',
            'category': self.category,  
            'start_date_time': self.start_date_time+' 20:20',
            'final_date_time': self.final_date_time+' 20:20'
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='description', errors='Este campo é obrigatório.')

    def test_missing_category_field(self):
        data = {
            'title': 'Título 1',
            'description': 'Descrição qualquer',
            'start_date_time': self.start_date_time+' 20:20',
            'final_date_time': self.final_date_time+' 20:20'
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='category', errors='Este campo é obrigatório.')

    def test_missing_start_date_time_field(self):
        data = {
            'title': 'Título 1',
            'description': 'Descrição qualquer',
            'category': self.category,  
            'final_date_time': self.final_date_time+' 20:20'
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='start_date_time', errors='Este campo é obrigatório.')

    def test_missing_final_date_time_field(self):
        data = {
            'title': 'Título 1',
            'description': '',
            'category': self.category,  
            'start_date_time': self.start_date_time+' 20:20',
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='final_date_time', errors='Este campo é obrigatório.')

    def test_category_choice_was_not_valid(self):
        data = {
            'title': 'Título 1',
            'description': 'Descrição qualquer',
            'category': 99,  
            'start_date_time': self.start_date_time+' 20:20',
            'final_date_time': self.final_date_time+' 20:20'
        }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='category', errors='Faça uma escolha válida. Sua escolha não é uma das disponíveis.')


