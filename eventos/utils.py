from django.contrib import messages
from django.contrib.messages import constants

def user_is_organizer(request, event, user):
    if event.organizer == user:
        return True
    else: 
        messages.add_message(request, constants.ERROR, 'Algo deu errado.')
        return False