from django.contrib.messages import constants
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.shortcuts import  redirect
from .tokens import account_activation_token
from core.settings import ENVIRONMENT

def need_set_age(request, user):
    if not user.idade:
        messages.add_message(request, constants.WARNING,'Para realizar tal ação <b>é preciso informar sua idade</b>.')
        return True
    return False

def activateEmail(request, user, to_email):
    if request.user.is_active:
        return redirect('home')
    email_subject = 'Ative sua Conta'
    context ={
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }
    if ENVIRONMENT == 'development':
        context['domain'] = 'localhost:8000'
    message = render_to_string('account/email/activate_account.html', context)
    email = EmailMessage(email_subject, message, to=[to_email])
    if email.send():
        message = f'Senhor <b>{user}</b>, por favor, vá até sua caixa de mensagens em seu email <b>{to_email}</b> e clique no link de ativação de conta para completar seu cadastro. <b>Nota:</b> Verifique sua caixa de spam.'
    else:
        message = f'Houve um problema ao tentar enviar o email de ativação para: {to_email}, verifique se o e-mail se foi digitado corretamente e tente novamente <a href="account/login/">login</a>.'
    
    request.session['activation_message'] = message
 