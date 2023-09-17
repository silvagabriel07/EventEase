from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..views import User
from ..models import Event, Category, Solicitation
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
            description='description etc', 
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
            description='description etc', 
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
            description='description etc', 
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
            description='description etc', 
            organizer=another_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time
        )
        response = self.client.get(reverse('editar_evento', args=[another_event.id]))
        self.assertRedirects(response, reverse('organizando'))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Algo deu errado.')

        
    def test_edition_not_available_for_past_events(self):
        self.any_event.start_date_time -= timedelta(days=3)
        self.any_event.final_date_time -= timedelta(days=5)
        self.any_event.save()

        response = self.client.get(reverse('editar_evento', args=[self.any_event.id]))
        self.assertRedirects(response, reverse('organizando'))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), f'Não é possível editar o evento "{self.any_event.title}", pois ele já passou.')
    
    def test_editar_evento_ok_get(self):
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
            description='description etc', 
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
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Algo deu errado.')


    def test_excluir_evento_ok_get(self):
        self.any_user.is_active = True
        self.any_user.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('excluir_evento', args=[self.any_event.id]))
        self.assertFalse(Event.objects.filter(id=self.any_event.id).exists())        
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), f'Evento {self.any_event.title} excluído com sucesso.')


class TestViewSolicitacoesEvento(TestCase):
    
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
            description='description etc', 
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
        response = self.client.get(reverse('solicitacoes_evento', args=[self.any_event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('organizando'))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Algo deu errado.')

    
    def test_solicitacoes_event_ok_get(self):
        self.any_user.is_active = True
        self.any_user.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('solicitacoes_evento', args=[self.any_event.id]))
        self.assertEqual(response.status_code, 200)        
    
    def test_solicitacoes_event_ok_rendered_solicitations(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=34, 
        )
        another_user_2 = User.objects.create_user(
            username='user 3', 
            password='senhaqualquer12', 
            email='email3@gmail.com', 
            idade=18, 
        )
        Solicitation.objects.create(user=another_user_2, event=self.any_event)
        Solicitation.objects.create(user=another_user, event=self.any_event)
        
        self.any_user.is_active = True
        self.any_user.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('solicitacoes_evento', args=[self.any_event.id]))
        any_event_solicitations = Solicitation.objects.filter(event=self.any_event)
        rendered_solicitations = response.context['solicitations']
        self.assertEqual(list(rendered_solicitations), list(any_event_solicitations))
        
    def test_search_input_solicitacoes_event_ok(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=34, 
        )
        another_user_2 = User.objects.create_user(
            username='user 3', 
            password='senhaqualquer12', 
            email='email3@gmail.com', 
            idade=18, 
        )
        Solicitation.objects.create(user=another_user_2, event=self.any_event)
        Solicitation.objects.create(user=another_user, event=self.any_event)
        
        self.any_user.is_active = True
        self.any_user.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(path=reverse('solicitacoes_evento', args=[self.any_event.id]), data={'search-input': 'user 2'})
        any_event_solicitations = Solicitation.objects.filter(event=self.any_event, user=another_user, status='w')
        rendered_solicitations = response.context['solicitations']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(rendered_solicitations), list(any_event_solicitations))

    def test_search_select_status_solicitacoes_event_ok(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=34, 
        )
        another_user_2 = User.objects.create_user(
            username='user 3', 
            password='senhaqualquer12', 
            email='email3@gmail.com', 
            idade=18, 
        )
        Solicitation.objects.create(user=another_user_2, event=self.any_event, status='a')
        Solicitation.objects.create(user=another_user, event=self.any_event, status='r')
        
        self.any_user.is_active = True
        self.any_user.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(path=reverse('solicitacoes_evento', args=[self.any_event.id]), data={'status_select': 'a'})
        any_event_solicitations = Solicitation.objects.filter(event=self.any_event, status='a')
        rendered_solicitations = response.context['solicitations']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(rendered_solicitations), list(any_event_solicitations))

    def test_search_input_and_search_select_status_solicitacoes_event_ok(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=34, 
        )
        another_user_2 = User.objects.create_user(
            username='user 3', 
            password='senhaqualquer12', 
            email='email3@gmail.com', 
            idade=18, 
        )
        Solicitation.objects.create(user=another_user_2, event=self.any_event, status='r')
        Solicitation.objects.create(user=another_user, event=self.any_event, status='r')
        
        self.any_user.is_active = True
        self.any_user.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(path=reverse('solicitacoes_evento', args=[self.any_event.id]), data={'search-input': 'user 3', 'status_select': 'r'})
        any_event_solicitations = Solicitation.objects.filter(event=self.any_event, user=another_user_2, status='r')
        rendered_solicitations = response.context['solicitations']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(rendered_solicitations), list(any_event_solicitations))

    def test_status_select_empty_found_solicitation_with_w_status(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=34, 
        )
        Solicitation.objects.create(user=another_user, event=self.any_event, status='a')
        
        self.any_user.is_active = True
        self.any_user.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get(path=reverse('solicitacoes_evento', args=[self.any_event.id]))
        any_event_solicitations = Solicitation.objects.filter(event=self.any_event, status='w')
        rendered_solicitations = response.context['solicitations']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(rendered_solicitations), list(any_event_solicitations))


class TestRejeitarSolicitacao(TestCase):
    
    def setUp(self) -> None:
        self.start_date_time = datetime.now() + timedelta(days=2)
        self.final_date_time = datetime.now() + timedelta(days=4)
        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=29, 
            is_active=True
        )
        

        Category.objects.create(name='Categoria A')
        self.any_event = Event.objects.create(
            title='Titulo 1', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        self.another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=18, 
        )
        self.another_user.is_active = True
        self.another_user.save()
        Solicitation.objects.create(event=self.any_event, user=self.another_user)

    
    def test_user_is_not_the_event_organizer(self):
        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('rejeitar_solicitacao', args=[self.any_event.id, self.another_user.id]))
        self.assertTrue(Solicitation.objects.exists())
        self.assertRedirects(response, reverse('organizando'))
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Algo deu errado.')
    
    def test_rejeitar_solicitacao_event_has_passed(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        self.any_event.final_date_time = datetime.now().replace(tzinfo=timezone.utc) - timedelta(days=2) 
        self.any_event.save()    
        response = self.client.get(reverse('rejeitar_solicitacao', args=[self.any_event.id, self.another_user.id]))
        self.assertEqual(Solicitation.objects.first().status, 'w')
        
        self.assertRedirects(response, reverse('organizando'))
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Não é possível rejeitar solicitações de usuários do evento "{self.any_event.title}", pois ele já passou.')

    def test_rejeitar_solicitacao_event_not_private(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        self.any_event.private = False
        self.any_event.save()
        response = self.client.get(reverse('rejeitar_solicitacao', args=[self.any_event.id, self.another_user.id]))
        self.assertRedirects(response, reverse('organizando'))

    def test_rejeitar_solicitacao_successfully(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('rejeitar_solicitacao', args=[self.any_event.id, self.another_user.id]))
        self.assertRedirects(response, reverse('solicitacoes_evento', args=[self.any_event.id]))
        self.assertEqual(Solicitation.objects.first().status, 'r')
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Solicitação <b>rejeitada</b> com sucesso.')

    def test_rejeitar_solicitacao_user_did_not_solicitate_for_this_event(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('rejeitar_solicitacao', args=[self.any_event.id, self.any_user.id]))
        self.assertRedirects(response, reverse('solicitacoes_evento', args=[self.any_event.id]))
        self.assertEqual(Solicitation.objects.first().status, 'w')
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Usuário em questão não solicitou participação para este evento')


class TestAceitarSolicitacao(TestCase):
    
    def setUp(self) -> None:
        self.start_date_time = datetime.now() + timedelta(days=2)
        self.final_date_time = datetime.now() + timedelta(days=4)
        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=29, 
            is_active=True
        )
        

        Category.objects.create(name='Categoria A')
        self.any_event = Event.objects.create(
            title='Titulo 1', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=True, 
            free=False,             
            start_date_time=self.start_date_time, 
            final_date_time=self.final_date_time, 
        )
        self.another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=18, 
        )
        self.another_user.is_active = True
        self.another_user.save()
        Solicitation.objects.create(event=self.any_event, user=self.another_user)

    
    def test_user_is_not_the_event_organizer(self):
        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('rejeitar_solicitacao', args=[self.any_event.id, self.another_user.id]))
        self.assertTrue(Solicitation.objects.exists())
        self.assertRedirects(response, reverse('organizando'))
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Algo deu errado.')
    
    def test_aceitar_solicitacao_event_has_passed(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        self.any_event.final_date_time = datetime.now().replace(tzinfo=timezone.utc) - timedelta(days=2) 
        self.any_event.save()    
        response = self.client.get(reverse('aceitar_solicitacao', args=[self.any_event.id, self.another_user.id]))
        self.assertEqual(Solicitation.objects.first().status, 'w')
        
        self.assertRedirects(response, reverse('organizando'))
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Não é possível aceitar solicitações de usuários do evento "{self.any_event.title}", pois ele já passou.')

    def test_aceitar_solicitacao_event_not_private(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        self.any_event.private = False
        self.any_event.save()
        response = self.client.get(reverse('aceitar_solicitacao', args=[self.any_event.id, self.another_user.id]))
        self.assertRedirects(response, reverse('organizando'))

    def test_aceitar_solicitacao_successfully(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('aceitar_solicitacao', args=[self.any_event.id, self.another_user.id]))
        self.assertRedirects(response, reverse('solicitacoes_evento', args=[self.any_event.id]))
        self.assertEqual(Solicitation.objects.first().status, 'a')
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Solicitação <b>aceita</b> com sucesso.')

    def test_aceitar_solicitacao_user_did_not_solicitate_for_this_event(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('aceitar_solicitacao', args=[self.any_event.id, self.any_user.id]))
        self.assertRedirects(response, reverse('solicitacoes_evento', args=[self.any_event.id]))
        self.assertEqual(Solicitation.objects.first().status, 'w')
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Usuário em questão não solicitou participação para este evento')

    def test_aceitar_solicitacao_from_a_banned_user_unban_the_user(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        self.any_event.banned_users.add(self.another_user)
        response = self.client.get(reverse('aceitar_solicitacao', args=[self.any_event.id, self.another_user.id]))
        self.assertEqual(self.any_event.banned_users.all().count(), 0)
        self.assertRedirects(response, reverse('solicitacoes_evento', args=[self.any_event.id]))
        self.assertEqual(Solicitation.objects.first().status, 'a')
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Solicitação <b>aceita</b> com sucesso.')


class TestViewVerMais(TestCase):
    
    def setUp(self) -> None:
        self.start_date_time = datetime.now() + timedelta(days=2)
        self.final_date_time = datetime.now() + timedelta(days=4)
        self.any_user = User.objects.create_user(
            username='user 1', 
            password='senhaqualquer12', 
            email='email@gmail.com', 
            idade=29, 
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

    
    def test_ver_evento_event_public_with_unauthenticated_user(self):
        response = self.client.get(reverse('ver_mais', args=[self.any_event.id]))
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertFalse(context.get('is_user_participant'))
        self.assertFalse(context.get('user_already_solicited'))
        self.assertFalse(context.get('is_banned_user'))
        
        btn_expected_url = reverse('account_login')
        self.assertContains(response, f'href="{btn_expected_url}">Participar</a>')

    def test_ver_evento_event_private_with_unauthenticated_user(self):
        self.any_event.private = True
        self.any_event.save()
        
        response = self.client.get(reverse('ver_mais', args=[self.any_event.id]))
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertFalse(context.get('is_user_participant'))
        self.assertFalse(context.get('user_already_solicited'))
        self.assertFalse(context.get('is_banned_user'))
        
        btn_expected_url = reverse('account_login')
        self.assertContains(response, f'href="{btn_expected_url}">Solicitar Participação</a>')

    
    def test_authenticated_user_get_view(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=18,
            is_active=True 
        )
        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('ver_mais', args=[self.any_event.id]))
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertFalse(context.get('is_user_participant'))
        self.assertFalse(context.get('user_already_solicited'))
        self.assertFalse(context.get('is_banned_user'))
        
        btn_expected_url = reverse('participar', args=[self.any_event.id])
        self.assertContains(response, f'href="{btn_expected_url}">Participar</a>')

    def test_authenticated_user_is_participant(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=18,
            is_active=True 
        )
        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        
        self.any_event.participants.add(another_user)

        response = self.client.get(reverse('ver_mais', args=[self.any_event.id]))
        context = response.context
        self.assertTrue(context.get('is_user_participant'))
        self.assertFalse(context.get('is_banned_user'))
        self.assertFalse(context.get('user_already_solicited'))

        self.assertContains(response, f'href="#">Já participa</button>')
    
    
    def test_authenticated_user_already_solicited(self):
        self.any_event.private = True
        self.any_event.save()
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=18,
            is_active=True 
        )
        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        Solicitation.objects.create(event=self.any_event, user=another_user)
        response = self.client.get(reverse('ver_mais', args=[self.any_event.id]))
        context = response.context
        self.assertTrue(context.get('user_already_solicited'))
        self.assertFalse(context.get('is_user_participant'))
        self.assertFalse(context.get('is_banned_user'))
        
        self.assertContains(response, f'href="#">Já Solicitou Participação</button>')
    
    def test_authenticated_user_is_banned_and_the_event_is_public(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=18,
            is_active=True 
        )
        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        self.any_event.banned_users.add(another_user)
        response = self.client.get(reverse('ver_mais', args=[self.any_event.id]))
        context = response.context
        self.assertFalse(context.get('user_already_solicited'))
        self.assertFalse(context.get('is_user_participant'))
        self.assertTrue(context.get('is_banned_user'))
        
        btn_expected_url = reverse('participar', args=[self.any_event.id])
        self.assertContains(response, f'href="{btn_expected_url}">Solicitar Participação</a>')

    def test_authenticated_user_is_banned_and_the_event_is_private(self):
        self.any_event.private = True
        self.any_event.save()
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=18,
            is_active=True 
        )
        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        self.any_event.banned_users.add(another_user)
        response = self.client.get(reverse('ver_mais', args=[self.any_event.id]))
        context = response.context
        self.assertFalse(context.get('user_already_solicited'))
        self.assertFalse(context.get('is_user_participant'))
        self.assertTrue(context.get('is_banned_user'))
        
        btn_expected_url = reverse('participar', args=[self.any_event.id])
        self.assertContains(response, f'href="{btn_expected_url}">Solicitar Participação</a>')

    def test_user_is_minor_and_the_event_is_not_free(self):
        another_user = User.objects.create_user(
            username='user 2', 
            password='senhaqualquer12', 
            email='email2@gmail.com', 
            idade=13,
            is_active=True 
        )
        self.client.login(email='email2@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('ver_mais', args=[self.any_event.id]))
        context = response.context
        self.assertFalse(context.get('user_already_solicited'))
        self.assertFalse(context.get('is_user_participant'))
        self.assertFalse(context.get('is_banned_user'))
        
        self.assertContains(response, 'href="#">Participar</button>')
        self.assertContains(response, 'Você não pode participar deste evento, pois ele é para maiores de idade.')

    def test_user_authenticated_is_organizer(self):
        self.client.force_login(self.any_user)
        response = self.client.get(reverse('ver_mais', args=[self.any_event.id]))
        
        context = response.context
        self.assertFalse(context.get('user_already_solicited'))
        self.assertFalse(context.get('is_user_participant'))
        self.assertFalse(context.get('is_banned_user'))

        btn_expected_url = reverse('participar', args=[self.any_event.id])
        self.assertContains(response, f'href="{btn_expected_url}">Participar</a>')

    def test_ver_evento_event_has_already_passed(self):
        self.any_event.final_date_time -= timedelta(days=5)
        self.any_event.start_date_time -= timedelta(days=3)
        self.any_event.save()        
        response = self.client.get(reverse('ver_mais', args=[self.any_event.id]))
        
        self.assertNotContains(response, 'btn cta-button')
        self.assertContains(response, 'Evento já passou...')


class TestViewParticipantes(TestCase):
    
    def setUp(self) -> None:
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
            email='email2@gmail.com', 
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
        self.any_event.participants.add(self.another_user)

    def test_participantes_render_event_participants_correcly(self):
        response = self.client.get(reverse('participantes', args=[self.any_event.id]))
        self.assertEqual(response.status_code, 200)
        all_participants = list(self.any_event.participants.all())
        self.assertEqual(list(response.context.get('participants')), all_participants)

    def test_participantes_render_qtd_event_participants_correcly(self):
        response = self.client.get(reverse('participantes', args=[self.any_event.id]))
        self.assertEqual(response.status_code, 200)
        total_participants = self.any_event.participants.all().count()
        self.assertEqual(response.context.get('qtd_participants'), total_participants)

    def test_participantes_render_search_event_participants_correcly(self):
        response = self.client.get(reverse('participantes', args=[self.any_event.id]), data={'search-input': 'a'})
        self.assertEqual(response.status_code, 200)
        all_participants = list(self.any_event.participants.filter(username__icontains='a'))
        self.assertEqual(list(response.context.get('participants')), all_participants)
        
    def test_participantes_organizer_event(self):
        self.client.force_login(self.any_user)
        response = self.client.get(reverse('participantes', args=[self.any_event.id]))
        url_remover_participante = reverse('remover_participante', args=[self.any_event.id, self.another_user.id])
        self.assertContains(response, f'href="{url_remover_participante}">Expulsar</a>')


class TestViewRemoverParticipante(TestCase):
    
    def setUp(self) -> None:
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
        self.any_event.participants.add(self.another_user)

    def test_user_is_not_the_event_organizer(self):        
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        url = reverse('remover_participante', args=[self.any_event.id, self.another_user.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('participantes', args=[self.any_event.id]))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Algo deu errado.')

    def test_remover_participante_from_event_has_already_passed(self):
        self.any_event.start_date_time -= timedelta(days=3)
        self.any_event.final_date_time -= timedelta(days=5)
        self.any_event.save()
        self.client.login(email='email@gmail.com', password='senhaqualquer12')

        url = reverse('remover_participante', args=[self.any_event.id, self.another_user.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('organizando'))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Não é possível remover usuários do evento "{self.any_event.title}", pois ele já passou.')
        
    def test_remover_participante_successfully_user_becomes_banned_user(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        url = reverse('remover_participante', args=[self.any_event.id, self.another_user.id])
        response = self.client.get(url)
        self.assertEqual(self.any_event.banned_users.first(), self.another_user)
        
    def test_remover_participante_successfully_removes_the_user_from_the_event(self):
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        url = reverse('remover_participante', args=[self.any_event.id, self.another_user.id])
        response = self.client.get(url)
        self.assertFalse(self.any_event.participants.exists())
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Usuário removido com sucesso.')

    def test_remover_participante_successfully_delete_the_user_solicitation(self):
        Solicitation.objects.create(user=self.another_user, event=self.any_event, status='a')
        self.client.login(email='email@gmail.com', password='senhaqualquer12')
        url = reverse('remover_participante', args=[self.any_event.id, self.another_user.id])
        response = self.client.get(url)
        self.assertEqual(self.any_event.solicitation_set.all().count(), 0)
        

class TestViewParticipar(TestCase):
    
    def setUp(self) -> None:
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
        
    def test_participar_public_event_has_already_passed(self):
        self.any_event.start_date_time -= timedelta(days=3)
        self.any_event.final_date_time -= timedelta(days=5)
        self.any_event.save()
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participar', args=[self.any_event.id]))
        self.assertRedirects(response, reverse('ver_mais', args=[self.any_event.id]))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Não é possível participar do evento "{self.any_event.title}", pois ele já passou.')
        self.assertEqual(self.any_event.participants.all().count(), 0)
        
    def test_participar_private_event_has_already_passed(self):
        self.any_event.private = True
        self.any_event.start_date_time -= timedelta(days=3)
        self.any_event.final_date_time -= timedelta(days=5)
        self.any_event.save()
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participar', args=[self.any_event.id]))
        self.assertRedirects(response, reverse('ver_mais', args=[self.any_event.id]))
        msgs =  list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Não é possível solicitar partipação para o evento "{self.any_event.title}", pois ele já passou.')
        self.assertEqual(self.any_event.solicitation_set.all().count(), 0)
        
    def test_participar_user_is_already_a_participant_in_the_event(self):
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        self.any_event.participants.add(self.another_user)
        response = self.client.get(reverse('participar', args=[self.any_event.id]))
        
        self.assertRedirects(response, reverse('ver_mais', args=[self.any_event.id]))
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Você já participa deste evento.')
        self.assertEqual(self.any_event.solicitation_set.all().count(), 0)

    def test_participar_not_free_event_and_user_need_set_age(self):
        self.any_event.free = False
        self.any_event.save()
        self.another_user.idade = None
        self.another_user.save()
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participar', args=[self.any_event.id]))
        self.assertRedirects(response, reverse('perfil'))
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Para realizar tal ação <b>é preciso informar sua idade</b>.')
        

    def test_participar_not_free_event_and_user_is_minor(self):
        self.any_event.free = False
        self.any_event.save()
        self.another_user.idade = 17
        self.another_user.save()
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participar', args=[self.any_event.id]))
        self.assertRedirects(response, reverse('ver_mais', args=[self.any_event.id]))
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), 'Você não pode participar deste evento, pois ele é apenas para maiores de idade.')

    def test_participar_public_event_as_a_banned_user_solicits_a_participation(self):
        self.any_event.banned_users.add(self.another_user)
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participar', args=[self.any_event.id]))
        self.assertRedirects(response, reverse('ver_mais', args=[self.any_event.id]))
        self.assertTrue(self.any_event.solicitation_set.all().exists())
        self.assertFalse(self.any_event.participants.all().exists())
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Solicitação realizada com sucesso, aguarde a reposta.')

    def test_participar_private_event_as_a_banned_user_solicits_a_participation(self):
        self.any_event.private = True
        self.any_event.save()
        self.any_event.banned_users.add(self.another_user)
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participar', args=[self.any_event.id]))
        self.assertRedirects(response, reverse('ver_mais', args=[self.any_event.id]))
        self.assertTrue(self.any_event.solicitation_set.all().exists())
        self.assertFalse(self.any_event.participants.all().exists())
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Solicitação realizada com sucesso, aguarde a reposta.')

    def test_participar_solicitate_participation_in_the_private_event_successfully(self):
        self.any_event.private = True
        self.any_event.save()
        self.client.login(email='another@gmail.com', password='senhaqualquer12')

        response = self.client.get(reverse('participar', args=[self.any_event.id]))
        self.assertEqual(self.any_event.solicitation_set.all().count(), 1)
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Solicitação realizada com sucesso, aguarde a reposta.')
        self.assertRedirects(response, reverse('ver_mais', args=[self.any_event.id]))

    def test_participar_public_event_successfully(self):
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participar', args=[self.any_event.id]))
        self.assertEqual(self.any_event.participants.all().count(), 1)
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Você está participando do evento <b>{self.any_event.title}</b>')
        self.assertRedirects(response, reverse('ver_mais', args=[self.any_event.id]))

    def test_participar_private_event_user_has_already_solicited_participation_in_the_event(self):
        self.any_event.private = True
        self.any_event.save()
        Solicitation.objects.create(user=self.any_user, event=self.any_event)
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participar', args=[self.any_event.id]))
        self.assertRedirects(response, reverse('ver_mais', args=[self.any_event.id]))
        self.assertEqual(self.any_event.solicitation_set.all().couont(), 1)
        msgs = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(msgs[0]), f'Algo deu errado. Verifique se você já não solicitou a participação para este evento')
        

class TestViewParticipando(TestCase):
    
    def setUp(self) -> None:
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
    
    # tests about rendering of event solicitations 
    def test_participando_see_event_solicitation_correctly(self):
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        Solicitation.objects.create(user=self.another_user, event=self.any_event)  
           
        response = self.client.get(reverse('participando', args=[1]))
        self.assertEqual(response.status_code, 200)
        expected_solicitations = Event.objects.filter(id=self.any_event.id)
        self.assertEqual(list(response.context.get('events')), list(expected_solicitations))
        expected_url = reverse('participando', args=[0])
        self.assertContains(response, f'href="{expected_url}">Participando ▼</a>')
        
    def test_participando_see_event_solicitations_that_ended_yeasterday(self):
        any_event2 = Event.objects.create(
            title='Titulo 2', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=datetime.now() - timedelta(days=2), 
            final_date_time=datetime.now() - timedelta(days=1), 
        )
        self.any_event.start_date_time = datetime.now() - timedelta(days=3)
        self.any_event.final_date_time = datetime.now() - timedelta(days=2)
        self.any_event.save()
        Solicitation.objects.create(user=self.another_user, event=self.any_event)
        Solicitation.objects.create(user=self.another_user, event=any_event2)
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participando', args=[1]))
        self.assertEqual(response.status_code, 200)
        # i  did this just so that any_event is a queryset
        expected_solicitations = Event.objects.filter(id=any_event2.id)
        self.assertEqual(list(response.context.get('events')), list(expected_solicitations))
        self.assertContains(response, 'Evento já acabou...')


    def test_participando_see_event_solicitations_that_ended_yeasterday_with_status_solicitation_filter(self):
        any_event2 = Event.objects.create(
            title='Titulo 2', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=datetime.now() - timedelta(days=2), 
            final_date_time=datetime.now() - timedelta(days=1), 
        )
        any_event3 = Event.objects.create(
            title='Titulo 3', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=datetime.now() - timedelta(days=2), 
            final_date_time=datetime.now() - timedelta(days=1), 
        )
        self.any_event.start_date_time = datetime.now() - timedelta(days=3)
        self.any_event.final_date_time = datetime.now() - timedelta(days=2)
        self.any_event.save()
        Solicitation.objects.create(user=self.another_user, event=self.any_event)
        Solicitation.objects.create(user=self.another_user, event=any_event2)
        Solicitation.objects.create(user=self.another_user, event=any_event3, status='r')
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participando', args=[1]), data={'select_status_solicitation': 'r'})
        self.assertEqual(response.status_code, 200)
        # i  did this just so that any_event is a queryset
        expected_solicitations = Event.objects.filter(id=any_event3.id)
        self.assertEqual(list(response.context.get('events')), list(expected_solicitations))

    # tests about rendering of participating events
    def test_participando_see_participanting_events_correctly(self):
        self.any_event.participants.add(self.another_user)
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
           
        response = self.client.get(reverse('participando', args=[0]))
        self.assertEqual(response.status_code, 200)
        expected_solicitations = Event.objects.filter(id=self.any_event.id)
        self.assertEqual(list(response.context.get('events')), list(expected_solicitations))
        expected_url = reverse('participando', args=[1])
        self.assertContains(response, f'href="{expected_url}">Solicitações ▲</a>')

    def test_participando_see_participanting_events_that_ended_yeasterday(self):
        any_event2 = Event.objects.create(
            title='Titulo 2', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=datetime.now() - timedelta(days=2), 
            final_date_time=datetime.now() - timedelta(days=1), 
        )
        self.any_event.start_date_time = datetime.now() - timedelta(days=3)
        self.any_event.final_date_time = datetime.now() - timedelta(days=2)
        self.any_event.save()
        self.any_event.participants.add(self.another_user)
        any_event2.participants.add(self.another_user)
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participando', args=[0]))
        self.assertEqual(response.status_code, 200)
        # i  did this just so that any_event is a queryset
        expected_solicitations = Event.objects.filter(id=any_event2.id)
        self.assertEqual(list(response.context.get('events')), list(expected_solicitations))
        self.assertContains(response, 'Evento já acabou...')

    def test_participando_see_participanting_events_with_decrescent_and_title_order_filter(self):
        any_event2 = Event.objects.create(
            title='Z Título 2', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=datetime.now() + timedelta(days=2), 
            final_date_time=datetime.now() + timedelta(days=1), 
        )
        any_event2.participants.add(self.another_user)
        self.any_event.participants.add(self.another_user)
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
           
        response = self.client.get(reverse('participando', args=[0]), data={'select_dec_cre': 'decrescent'})
        self.assertEqual(response.status_code, 200)
        expected_order = ['Z Título 2', 'Titulo 1']
        self.assertQuerysetEqual(response.context.get('events'), expected_order, transform=lambda x: x.title)
        
    def test_participando_see_participanting_events_with_crescent_and_title_order_filter(self):
        any_event2 = Event.objects.create(
            title='Z Título 2', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=datetime.now() + timedelta(days=2), 
            final_date_time=datetime.now() + timedelta(days=1), 
        )
        any_event2.participants.add(self.another_user)
        self.any_event.participants.add(self.another_user)
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
           
        response = self.client.get(reverse('participando', args=[0]), data={'select_dec_cre': 'crescent'})
        self.assertEqual(response.status_code, 200)
        expected_order = ['Titulo 1', 'Z Título 2']
        self.assertQuerysetEqual(response.context.get('events'), expected_order, transform=lambda x: x.title)

    def test_participando_see_participanting_events_with_start_date_time_order_filter(self):
        any_event2 = Event.objects.create(
            title='Z Título 2', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=datetime.now() + timedelta(days=1), 
            final_date_time=datetime.now() + timedelta(days=2), 
        )
        self.any_event.start_date_time = datetime.now() + timedelta(days=3)
        self.any_event.start_date_time = datetime.now() + timedelta(days=4)
        self.any_event.save()
        
        any_event2.participants.add(self.another_user)
        self.any_event.participants.add(self.another_user)
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
           
        response = self.client.get(reverse('participando', args=[0]), data={'select_order': 'start_date_time'})
        self.assertEqual(response.status_code, 200)
        expected_order = ['Z Título 2', 'Titulo 1']
        self.assertQuerysetEqual(response.context.get('events'), expected_order, transform=lambda x: x.title)

    def test_participando_see_participanting_events_with_num_participants_order_filter(self):
        any_user2 = User.objects.create_user(
            username='anyuser2', 
            password='senhaqualquer12', 
            email='email3@gmail.com', 
            idade=29, 
            is_active=True
        )

        any_event2 = Event.objects.create(
            title='Z Título 2', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=datetime.now() + timedelta(days=1), 
            final_date_time=datetime.now() + timedelta(days=2), 
        )
        self.any_event.start_date_time = datetime.now() + timedelta(days=3)
        self.any_event.start_date_time = datetime.now() + timedelta(days=4)
        self.any_event.save()
        
        any_event2.participants.add(self.another_user)        
        self.any_event.participants.add(self.another_user)
        # now, any_event has 2 participants
        self.any_event.participants.add(any_user2)

        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participando', args=[0]), data={'select_order': 'num_participants'})
        self.assertEqual(response.status_code, 200)
        expected_order = ['Z Título 2', 'Titulo 1']
        self.assertQuerysetEqual(response.context.get('events'), expected_order, transform=lambda x: x.title)

    def test_participando_see_participanting_events_with_invalid_filters(self):
        any_event2 = Event.objects.create(
            title='Z Título 2', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=False, 
            free=False,             
            start_date_time=datetime.now() + timedelta(days=1), 
            final_date_time=datetime.now() + timedelta(days=2), 
        )
        self.any_event.participants.add(self.another_user)
        any_event2.participants.add(self.another_user)        
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participando', args=[0]), data={'select_order': 'iaveib', 'select_dec_cre': '8163gdbiqn'})
        self.assertEqual(response.status_code, 200)
        # for default this is oredered by 'title' 'crescent'  
        expected_order = ['Titulo 1', 'Z Título 2']
        self.assertQuerysetEqual(response.context.get('events'), expected_order, transform=lambda x: x.title)

    def test_participando_see_event_solicitations_with_invalid_filters(self):
        any_event2 = Event.objects.create(
            title='Z Título 2', 
            description='description etc', 
            organizer=self.any_user, 
            category_id=1, 
            private=True, 
            free=True,
            start_date_time=datetime.now() + timedelta(days=1), 
            final_date_time=datetime.now() + timedelta(days=2), 
        )
        Solicitation.objects.create(event=self.any_event, user=self.another_user)
        Solicitation.objects.create(event=any_event2, user=self.another_user)
        self.client.login(email='another@gmail.com', password='senhaqualquer12')
        
        response = self.client.get(reverse('participando', args=[1]), data={'select_order': 'iaveib', 'select_dec_cre': '8163gdbiqn'})
        self.assertEqual(response.status_code, 200)
        # for default this is oredered by 'title' 'crescent'  
        expected_order = ['Titulo 1', 'Z Título 2']
        self.assertQuerysetEqual(response.context.get('events'), expected_order, transform=lambda x: x.title)
