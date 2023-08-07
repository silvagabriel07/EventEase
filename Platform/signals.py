from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from notifications.signals import notify
from eventos.models import Solicitation, Event
from account_manager.models import User

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
                verb=f'O usuário {user.username}, que <u>havia sido banido</u> do evento <a class="link" href="{ver_mais_url}">'+event.title+'</a>, solicitou participação',
                target=event,
                actions=actions
            )
        else:
            notify.send(user,
                recipient=event.organizer,
                verb=f'Solicitou participação para o evento <a class="link" href="{ver_mais_url}">'+event.title+'</a>.',
                target=event,
                actions=actions
            )

    else:
        if instance.status == 'a':
            extra_data = {'style': 'a'}

            notify.send(event.organizer,
                recipient=user,
                verb=f'Sua solicitação de participação para o evento <a class="link" href="{ver_mais_url}">'+event.title+'</a> foi <b>aceita</b>. Agora você participa do evento 😊',
                target=event,
                extra_data=extra_data,
                actions=actions
             )
        elif instance.status == 'r':
            extra_data ={'style': 'r'}

            notify.send(event.organizer,
                recipient=user,
                verb=f'Sua solicitação de participação para o evento <a class="link" href="{ver_mais_url}">'+event.title+'</a> foi <b>rejeitada</b>.',
                target=event,
                extra_data=extra_data,
                actions=actions
             )


@receiver(m2m_changed, sender=Event.participants.through)
def send_participant_notification(sender, instance, action, pk_set, **kwargs):
    ver_mais_url = f'http://127.0.0.1:8000/eventos/ver_mais/{instance.id}/'
    if action == 'post_remove':
        extra_data = {'style': 'removed'}
        for user_id in pk_set:
            user = User.objects.get(id=user_id)
            notify.send(instance.organizer, recipient=user, verb=f'Você foi removido do evento <a class="link" href="{ver_mais_url}">'+instance.title+'</a>.', target=instance, extra_data=extra_data)
