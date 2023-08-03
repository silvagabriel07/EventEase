from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Event
from django.db.models import Count, F
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Solicitation
from account_manager.utils import need_set_age
from account_manager.models import User
from .utils import user_is_organizer

# Create your views here.
@login_required
def organizando(request):    
    my_events = Event.objects.filter(organizer=request.user)
    return render(request, 'organizando.html', {'my_events': my_events})


@login_required
def criar_evento(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False) 
            event.organizer = request.user  
            event.save() 
            messages.success(request, 'Evento criado com sucesso.')
            return redirect('organizando')
    else:
        form = EventForm()

    return render(request, 'criar_evento.html', {'form': form})


@login_required
def editar_evento(request, event_id):        
    event = Event.objects.filter(id=event_id).first()
    if not user_is_organizer(request, event, request.user): 
        return redirect('organizando')
    else:
        event_banner = event.event_banner
        if request.method == 'POST':    
            form = EventForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                form.save()
                messages.add_message(request, constants.SUCCESS, 'Evento editado com sucesso.')
                return redirect('organizando')
        else:
            form = EventForm(instance=event)
                    
        return render(request, 'editar_evento.html', {'form': form, 'event_banner': event_banner, 'event_id': event.id})
    

@login_required
def solicitacoes_evento(request, event_id):
    event = Event.objects.filter(id=event_id).first()

    if not user_is_organizer(request, event, request.user): 
        return redirect('organizando')
    else:
        search = request.GET.get('search-input')
        status_select = request.GET.get('status_select', 'w')
        
        solicitations = event.solicitation_set.all()    
        if search:
            solicitations = solicitations.filter(user__username__icontains=search)
        if status_select:
            solicitations = solicitations.filter(status=status_select)
        return render(request, 'solicitacoes_evento.html', {'solicitations': solicitations, 'event_title': event.title})


def ver_mais(request, id_event):
    event = Event.objects.get(id=id_event)
    is_user_participant = False
    user_already_solicitated = False
    if request.user.is_authenticated:
        is_user_participant = request.user.is_user_participant(event)
        user_already_solicitated = request.user.user_already_solicitated(event)
        
    return render(request, 'ver_mais.html', {'event': event, 'is_user_participant': is_user_participant, 'user_already_solicitated': user_already_solicitated})


def participantes(request, id_event):
    event = Event.objects.get(id=id_event)
    participants = event.participants.all()
    is_organizer = False
    if user_is_organizer(request, event, request.user):
        is_organizer = True
    return render(request, 'participantes.html', {'participants': participants, 'event_title': event.title, 'user_is_organizer': is_organizer})


@login_required
def rejeitar_solicitacao(request, event_id, id_user_solicitation):
    event = Event.objects.filter(id=event_id).first()

    if not user_is_organizer(request, event, request.user) or not event.private:
        return redirect('organizando')
    else:
        if event.reject_user(user_id=id_user_solicitation):
            messages.add_message(request, constants.SUCCESS, 'Solicitação <b>rejeitada</b> com sucesso.')
        else:
            messages.add_message(request, constants.WARNING, 'Usuário em questão não solicitou participação para este evento')
        return redirect(reverse('solicitacoes_evento', args=[event.id])) 

@login_required
def aceitar_solicitacao(request, event_id, id_user_solicitation):
    event = Event.objects.filter(id=event_id).first()
    if not user_is_organizer(request, event, request.user) or not event.private:
        return redirect('organizando')
    else:
        if event.accept_user(user_id=id_user_solicitation):
            messages.add_message(request, constants.SUCCESS, 'Solicitação <b>aceita</b> com sucesso.')
        else:
            messages.add_message(request, constants.WARNING, 'Usuário em questão não solicitou participação para este evento')
        return redirect(reverse('solicitacoes_evento', args=[event_id])) 
 
# viewa de Partipar 
@login_required
def participar(request, id_event):
    user = request.user

    event = Event.objects.get(id=id_event)
    redirect_event_details = reverse('ver_mais', args=[id_event])

    if user.is_user_participant(event):
        messages.add_message(request, constants.ERROR, 'Você já participa deste evento.')
        return redirect(redirect_event_details)        

    if not event.free:
        if need_set_age(request, user):
            return redirect('profile')
        
        elif user.is_minor():
            messages.add_message(request, constants.ERROR, 'Você não pode participar deste evento, pois ele é apenas para maiores de idade.')
            return redirect(redirect_event_details)
                
    if not event.private or user_is_organizer(request, event, user):
            event.participants.add(user.id)
            event.save()
            messages.add_message(request, constants.SUCCESS, f'Você está participando do evento <b>{event.title}</b>')
    else:
        # solicitar a participação do evento privado 
        try:
            solicitation = Solicitation(
                user=user,
                event=event
            )
            solicitation.save()
            messages.add_message(request, constants.SUCCESS, 'Solicitação realizada com sucesso, aguarde a reposta.')
        except:
            messages.add_message(request, constants.ERROR, 'Algo deu errado. Verifique se você já não solicitou a participação para este evento')
    return redirect(redirect_event_details)


@login_required
def participando(request, render_solicitations=0):
    user = request.user

    if render_solicitations == 1:
        events = Event.objects.filter(solicitation__user=user)
        events = events.annotate(status_solicitation=F('solicitation__status'))
    else:
        events = Event.objects.filter(participants=user)
    order = request.GET.get('select_order', 'title')
    dec_or_cres = request.GET.get('select_dec_cre', 'crescent')
    
    if dec_or_cres == 'crescent':   
        dec_or_cres = ''
    else:
        dec_or_cres = '-'

    if order == 'num_participants':
        events = Event.objects.annotate(num_participants=Count('participants')).filter(participants=user) 
    
    order = f'{dec_or_cres}{order}'    
    events_sorted = events.order_by(order)
    return render(request, 'participando.html', {'events': events_sorted, 'render_solicitations': render_solicitations})


@login_required
def participando_solicitacoes(request):
    render_solicitations = 1
    participando_url_redirect = reverse('participando', args=[render_solicitations])
    return redirect(participando_url_redirect)


@login_required
def leave_event(request, event_id, render_solicitations=0):
    event = Event.objects.get(id=event_id)
    participando_url_redirect = reverse('participando', args=[render_solicitations])
    if render_solicitations == 1:
        solicitation_ = event.solicitation_set.get(user=request.user)
        solicitation_.delete()
        messages.add_message(request, constants.SUCCESS, f'Solicitação de participação para o evento <b>{event.title} removida com sucessa</b>')  
    else:
        event.participants.remove(request.user)
        event.save()
        messages.add_message(request, constants.SUCCESS, f'Você <b>removeu</b> sua participação no evento <b>{event.title}</b>')
    return redirect(participando_url_redirect)


