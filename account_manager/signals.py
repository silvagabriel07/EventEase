from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount

# means that if the user registers through a social account, their account becomes active.
@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    if SocialAccount.objects.filter(user=user).exists():
        user.username = user.email
        user.is_active = True
        user.save()
