from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.messages import constants
from django.contrib import messages
from .models import User
from django.contrib.auth import login

from allauth.account.views import LoginView, SignupView
# Create your views here.



class CustomSignupView(SignupView):
    def form_valid(self, form):
        user = form.save(self.request)
        
        if not user.is_active:
            activateEmail(self.request, user, user.email)
            return redirect('account_inactive')
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
        
        
class CustomLoginView(LoginView):
    def form_valid(self, form):
        email = form.cleaned_data['login']
        user = User.objects.get(email=email)        
        
        if not user.is_active:
            activateEmail(self.request, user, user.email)
            return redirect('account_inactive')
        return super().form_valid(form)
    

def activateEmail(request, user, to_email):
    if request.user.is_active:
        return redirect('home')
    email_subject = 'Ative sua Conta'
    message = render_to_string('account/email/activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(email_subject, message, to=[to_email])
    if email.send():
        message = f'Senhor <b>{user}</b>, por favor, vá até sua caixa de mensagens em seu email <b>{to_email}</b> e clique no link de ativação de conta para completar seu cadastro. <b>Nota:</b> Verifique sua caixa de spam.'
    else:
        message = f'Houve um problema ao tentar enviar o email de ativação para: {to_email}, verifique se o e-mail se foi digitado corretamente e tente novamente <a href="account/login/">login</a>.'
    
    request.session['activation_message'] = message
    return redirect('account_inactive')

def account_inactive(request):
    if request.user.is_active:
        return redirect('home')
    message = request.session.pop('activation_message', 'Esta conta está <b>desativada</b>. Verifique na caixa de mensagens do seu email se não enviamos um link para ativação. Se não foi enviado, tente logar novamente, verificando se o email foi digitado corretamente.')
    return render(request, 'account/account_inactive.html', {'message': message})

def activate_account(request, uidb64, token):
    if request.user.is_active:
        return redirect('home')
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        messages.add_message(request, constants.SUCCESS, 'Conta ativada e usuário logado com sucesso.')
        return redirect('home')
    else:
        messages.add_message(request, constants.ERROR, 'Link de ativação de conta inválido.')
        return redirect('account_inactive')
