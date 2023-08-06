from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from eventos.models import Solicitation

@receiver(post_save, sender=Solicitation)
def send_notification(sender, instance, created, **kwargs):
    actions = []
    
    if created:
        actions = [
            {'ver_participacoes_href': f'http://127.0.0.1:8000/eventos/organizando/solicitacoes_evento/{instance.event.id}/','title': 'Ver solicitações'},
        ]

        notify.send(instance.user,
                    recipient=instance.event.organizer,
                    verb=f'Solicitou participação para o evento <a class="link" href="http://127.0.0.1:8000/eventos/ver_mais/{instance.event.id}/">'+instance.event.title+'.</a>',
                    target=instance.event,
                    actions=actions
                    )
    else:
        if instance.status == 'a':
            extra_data = {'solicitation': 'a'}

            notify.send(instance.event.organizer,
             recipient=instance.user,
             verb=f'Sua solicitação de participação para o evento <a class="link" href="http://127.0.0.1:8000/eventos/ver_mais/{instance.event.id}/">'+instance.event.title+'.</a> foi <b>aceita</b>',
             target=instance.event,
             extra_data=extra_data,
             actions=actions
             )
        elif instance.status == 'r':
            extra_data ={'solicitation': 'r'}

            notify.send(instance.event.organizer,
             recipient=instance.user,
             verb=f'Sua solicitação de participação para o evento <a class="link" href="http://127.0.0.1:8000/eventos/ver_mais/{instance.event.id}/">'+instance.event.title+'</a> foi <b>rejeitada</b>.',
             target=instance.event,
             extra_data=extra_data,
             actions=actions
             )
