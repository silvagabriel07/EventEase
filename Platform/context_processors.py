from notifications.models import Notification

def notifications_count(request):
    if request.user.is_authenticated:
        # Obter a contagem de notificações não lidas do usuário atual
        count = Notification.objects.filter(recipient=request.user, unread=True).count()
        return {'notifications_count': count}
    else:
        return {}


