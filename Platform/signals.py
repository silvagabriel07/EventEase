from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from eventos.models import Solicitation

@receiver(post_save, sender=Solicitation)
def send_solicitation_notification(sender, instance, created, **kwargs):
    actions = []
    event = instance.event
    user = instance.user
    ver_mais_url = f'http://127.0.0.1:8000/eventos/ver_mais/{event.id}/'
    
    if created:
        actions = [
            {'ver_participacoes_href': f'http://127.0.0.1:8000/eventos/organizando/solicitacoes_evento/{event.id}/','title': 'Ver solicitações'},
        ]
        
        if event.is_banned_user(user.id):
            notify.send(user,
                recipient=event.organizer,
                verb=f'O usuário {user.username}, que <u>havia sido banido</u> do evento <a class="link" href="{ver_mais_url}">'+event.title+'.</a>, solicitou participação',
                target=event,
                actions=actions
            )
        else:
            notify.send(user,
                recipient=event.organizer,
                verb=f'Solicitou participação para o evento <a class="link" href="{ver_mais_url}">'+event.title+'.</a>',
                target=event,
                actions=actions
            )

    else:
        if instance.status == 'a':
            extra_data = {'solicitation': 'a'}

            notify.send(event.organizer,
                recipient=user,
                verb=f'Sua solicitação de participação para o evento <a class="link" href="{ver_mais_url}">'+event.title+'.</a> foi <b>aceita</b>',
                target=event,
                extra_data=extra_data,
                actions=actions
             )
        elif instance.status == 'r':
            extra_data ={'solicitation': 'r'}

            notify.send(event.organizer,
                recipient=user,
                verb=f'Sua solicitação de participação para o evento <a class="link" href="{ver_mais_url}">'+event.title+'</a> foi <b>rejeitada</b>.',
                target=event,
                extra_data=extra_data,
                actions=actions
             )
