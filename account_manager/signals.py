from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(user_signed_up)
def set_user_active(sender, **kwargs):
    user = kwargs['user']
    user.is_active = True
    user.save()
