from django.contrib import messages
from django.contrib.messages import constants

def user_is_organizer(request, event, message=True):
    if event.organizer == request.user:
        return True
    else: 
        if message:
            messages.add_message(request, constants.ERROR, 'Algo deu errado.')
        return False