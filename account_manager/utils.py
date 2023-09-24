from django.contrib.messages import constants
from django.contrib import messages

def need_set_age(request, user):
    if not user.idade:
        messages.add_message(request, constants.WARNING,'Para realizar tal ação <b>é preciso informar sua idade</b>.')
        return True
    return False
