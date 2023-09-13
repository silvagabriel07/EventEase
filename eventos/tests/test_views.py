from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..views import User
from ..models import Event, Category
from django.urls import reverse
from datetime import datetime, timezone, timedelta
from django.contrib import messages

class TestViewOrganizando(TestCase):
    
    def setUp(self) -> None:
        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=17, 
        )
        self.any_user.is_active = True
        self.any_user.save()
        
        self.start_date_time = datetime.now().replace(tzinfo=timezone.utc) + timedelta(days=1) 
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

        
    def test_organizing_events_render_organizing_events(self):
        self.assertTrue(self.client.login(email='email@gmail.com', password='senhaqualquer12'))
        response = self.client.get(reverse('organizando'))
        self.assertEqual(response.status_code, 200)
        # todos os eventos do user logado é o que esperamos
        another_user =  User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=17, 
        )
        # crio um outro evento para que tenha 2 eventos no BD
        Event.objects.create(
            title='Titulo 2', 
            description='descrition etc', 
            organizer=another_user, 
            category_id=1, 
            private=False, 
            free=False,
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        my_events = Event.objects.filter(organizer=self.any_user)
        self.assertEqual(list(response.context['my_events']), list(my_events))
        

class TestViewCriarEvento(TestCase):
    
    def setUp(self) -> None:
        self.start_date_time = (datetime.now() + timedelta(days=2)).strftime('%d/%m/%Y')
        self.final_date_time = (datetime.now() + timedelta(days=4)).strftime('%d/%m/%Y')
        self.uploaded_file = SimpleUploadedFile(
            name='event_banner.png',
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x06bKGD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\tpHYs\x00\x00\x0b\xf8\x00\x00\x0b\xf8\x01\xc7o\xa8d\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00\xc0\xc0\xc0\xf7\xf7\xf7\x00\x00\x00\xfc\x00\x00\x00\x00gAMA\x00\x00\xaf\xc8\x37\x05\x8a\xe9\x00\x00\x00\tpHYs\x00\x00\x0b\xf8\x00\x00\x0b\xf8\x01\xc7o\xa8d\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00\xc0\xc0\xc0\xf7\xf7\xf7\x00\x00\x00\xfc\x00\x00\x00\x00gAMA\x00\x00\xaf\xc8\x37\x05\x8a\xe9\x00\x00\x00\x1aIDATx\xda\xed\xc1\x01\x0d\x00\x00\x08\xc0\xc0\xec\x7fY\x00\x00\x00\x00IEND\xaeB`\x82',
            content_type='image/png'
        )
        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=29, 
        )
        self.any_user.is_active = True
        self.any_user.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        self.url = reverse('criar_evento')

        Category.objects.create(name='Categoria Qualquer')

    def test_criar_evento_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'criar_evento.html')

    
    def test_criar_evento_post_valid(self):
        form_data = {
            'title': 'Evento de Teste',
            'description': 'Descrição do evento de teste',
            'category': 1, 
            'start_date_time': self.start_date_time+' 14:00',
            'final_date_time': self.final_date_time+' 16:00',
        }

        # Crie um arquivo temporário simulado para o campo event_banner
        uploaded_file = SimpleUploadedFile(
            name='event_banner.jpg',
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x06bKGD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\tpHYs\x00\x00\x0b\xf8\x00\x00\x0b\xf8\x01\xc7o\xa8d\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00\xc0\xc0\xc0\xf7\xf7\xf7\x00\x00\x00\xfc\x00\x00\x00\x00gAMA\x00\x00\xaf\xc8\x37\x05\x8a\xe9\x00\x00\x00\tpHYs\x00\x00\x0b\xf8\x00\x00\x0b\xf8\x01\xc7o\xa8d\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00\xc0\xc0\xc0\xf7\xf7\xf7\x00\x00\x00\xfc\x00\x00\x00\x00gAMA\x00\x00\xaf\xc8\x37\x05\x8a\xe9\x00\x00\x00\x1aIDATx\xda\xed\xc1\x01\x0d\x00\x00\x08\xc0\xc0\xec\x7fY\x00\x00\x00\x00IEND\xaeB`\x82',
            content_type='image/png'
        )

        response = self.client.post(self.url, data=form_data, files={'event_banner': uploaded_file})

        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Event.objects.count(), 1)  
        self.assertRedirects(response, reverse('organizando'))  

    def test_criar_evento_post_invalid(self):
        form_data = {
            'title': 'Evento de Teste',
            # não passei description
            'category': 1, 
            'start_date_time': self.start_date_time+' 14:00',
            'final_date_time': self.final_date_time+' 16:00',
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.exists())  
        self.assertFormError(response, 'form', 'description', ['Este campo é obrigatório.']) 


class TestViewEditarEvento(TestCase):
    
    def setUp(self) -> None:
        self.start_date_time = datetime.now() + timedelta(days=2)
        self.final_date_time = datetime.now() + timedelta(days=4)
        self.uploaded_file = SimpleUploadedFile(
            name='event_banner.png',
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x06bKGD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\tpHYs\x00\x00\x0b\xf8\x00\x00\x0b\xf8\x01\xc7o\xa8d\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00\xc0\xc0\xc0\xf7\xf7\xf7\x00\x00\x00\xfc\x00\x00\x00\x00gAMA\x00\x00\xaf\xc8\x37\x05\x8a\xe9\x00\x00\x00\tpHYs\x00\x00\x0b\xf8\x00\x00\x0b\xf8\x01\xc7o\xa8d\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00\xc0\xc0\xc0\xf7\xf7\xf7\x00\x00\x00\xfc\x00\x00\x00\x00gAMA\x00\x00\xaf\xc8\x37\x05\x8a\xe9\x00\x00\x00\x1aIDATx\xda\xed\xc1\x01\x0d\x00\x00\x08\xc0\xc0\xec\x7fY\x00\x00\x00\x00IEND\xaeB`\x82',
            content_type='image/png'
        )
        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=29, 
        )
        self.any_user.is_active = True
        self.any_user.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')

        Category.objects.create(name='Categoria Qualquer')
        
        self.any_event = Event.objects.create(
            title='Titulo 1', 
            description='descrition etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time
        )

    
    def test_user_is_not_the_event_organizer(self):
        another_user = User.objects.create(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=19, 
        )
        another_event = Event.objects.create(
            title='Titulo 1', 
            description='descrition etc', 
            organizer=another_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time
        )
        response = self.client.get(reverse('editar_evento', args=[another_event.id]))
        self.assertRedirects(response, reverse('organizando'))
        
    def test_edition_not_available_for_past_events(self):
        self.any_event.start_date_time -= timedelta(days=3)
        self.any_event.final_date_time -= timedelta(days=5)
        self.any_event.save()

        response = self.client.get(reverse('editar_evento', args=[self.any_event.id]))
        self.assertRedirects(response, reverse('organizando'))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), f'Não é possível editar o evento "{self.any_event.title}", pois ele já passou.')
    
    def test_editar_evento_successful_get(self):
        response = self.client.get(reverse('editar_evento', args=[self.any_event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editar_evento.html')
    
    def test_editar_evento_valid_post(self):
        form_data = {
            'title': 'Evento de Teste',
            'description': 'Descrição do evento de teste',
            'category': 1, 
            'start_date_time': self.start_date_time.strftime('%d/%m/%Y')+' 14:00',
            'final_date_time': self.final_date_time.strftime('%d/%m/%Y')+' 16:00',
        }
        response = self.client.post(reverse('editar_evento', args=[self.any_user.id]), data=form_data)
        self.assertTrue(Event.objects.filter(title='Evento de Teste').exists())
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), 'Evento editado com sucesso.')
        self.assertRedirects(response, reverse('organizando'))

    
    def test_editar_evento_invalid_post(self):
        form_data = {
            'title': 'Evento de Teste',
            'description': 'Descrição do evento de teste',
            'category': 1, 
            'start_date_time': self.start_date_time.strftime('%Y/%d/%m')+' 14:00',
            'final_date_time': self.final_date_time.strftime('%d/%m/%Y')+' 16:00',
        }
        response = self.client.post(reverse('editar_evento', args=[self.any_user.id]), data=form_data)
        self.assertFalse(Event.objects.filter(title='Evento de Teste').exists())
        self.assertEqual(response.status_code, 200)
        # renderizado com os erros
        self.assertTemplateUsed(response, 'editar_evento.html')
        self.assertFormError(response, 'form', 'start_date_time', ['Informe a data e hora no formato solicitado: DD/MM/AAAA HH:MM']) 


class TestViewExcluirEvento(TestCase):
    
    def setUp(self) -> None:
        self.start_date_time = datetime.now() + timedelta(days=2)
        self.final_date_time = datetime.now() + timedelta(days=4)
        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=29, 
        )
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

    def test_user_is_not_the_event_organizer(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=18, 
        )
        another_user.is_active = True
        another_user.save()

        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('excluir_evento', args=[self.any_event.id]))
        self.assertTrue(Event.objects.filter(id=self.any_event.id).exists())

    def test_excluir_evento_successful_get(self):
        self.any_user.is_active = True
        self.any_user.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('excluir_evento', args=[self.any_event.id]))
        self.assertFalse(Event.objects.filter(id=self.any_event.id).exists())        
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), f'Evento {self.any_event.title} excluído com sucesso.')


