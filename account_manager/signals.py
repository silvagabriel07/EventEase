from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount

@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    if SocialAccount.objects.filter(user=user).exists():
        user.username = user.email
        user.is_active = True
        user.save()
