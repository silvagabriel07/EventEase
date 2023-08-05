from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from eventos.models import Solicitation

@receiver(post_save, sender=Solicitation)
def send_notification(sender, instance, created, **kwargs):
    if created:
        notify.send(instance.user, recipient=instance.event.organizer, verb=f'{instance.user.username} solicitou participação para o evento {instance.event.title}.', target=instance.event)
    elif instance.status == 'a':
        notify.send(instance.event.organizer, recipient=instance.user, verb=f'Sua solcitação de participação para o evento {instance.event.title} foi aceita.', target=instance.event)
    elif instance.status == 'r':
        notify.send(instance.event.organizer, recipient=instance.user, verb=f'Sua solcitação de participação para o evento {instance.event.title} foi rejeitada.', target=instance.event)
