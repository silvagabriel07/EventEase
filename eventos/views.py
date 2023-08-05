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
from .utils import user_is_organizer
from datetime import datetime, timedelta

# Views de organizando
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
    if not user_is_organizer(request, event): 
        return redirect('organizando')
    if event.has_passed():
        messages.add_message(request, constants.ERROR, f'Não é possível editar o evento "{event.title}", pois ele já passou.')
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
    

def excluir_evento(request, event_id):
    event = Event.objects.get(id=event_id)
    if user_is_organizer(request, event=event):
        event.delete()
        messages.add_message(request, constants.SUCCESS, f'Evento {event.title} excluído com sucesso.') 
    return redirect('organizando')


@login_required
def solicitacoes_evento(request, event_id):
    event = Event.objects.filter(id=event_id).first()

    if not user_is_organizer(request, event): 
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


@login_required
def rejeitar_solicitacao(request, event_id, id_user_solicitation):
    event = Event.objects.filter(id=event_id).first()
    
    if not user_is_organizer(request, event) or not event.private:
        return redirect('organizando')
    elif event.has_passed():
        messages.add_message(request, constants.ERROR, f'Não é possível rejeitar solicitações de usuários do evento "{event.title}", pois ele já passou.')
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
    if not user_is_organizer(request, event) or not event.private:
        return redirect('organizando')
    elif event.has_passed():
        messages.add_message(request, constants.ERROR, f'Não é possível aceitar solicitações de usuários do evento "{event.title}", pois ele já passou.')
        return redirect('organizando')

    else:
        if event.accept_user(user_id=id_user_solicitation):
            messages.add_message(request, constants.SUCCESS, 'Solicitação <b>aceita</b> com sucesso.')
        else:
            messages.add_message(request, constants.WARNING, 'Usuário em questão não solicitou participação para este evento')
        return redirect(reverse('solicitacoes_evento', args=[event_id])) 

# # # # #

def ver_mais(request, id_event):
    event = Event.objects.get(id=id_event)
    is_user_participant = False
    user_already_solicitated = False
    if request.user.is_authenticated:
        is_user_participant = request.user.is_user_participant(event)
        user_already_solicitated = request.user.user_already_solicitated(event)
        
    return render(request, 'ver_mais.html', {'event': event, 'is_user_participant': is_user_participant, 'user_already_solicitated': user_already_solicitated})


def participantes(request, event_id):
    event = Event.objects.get(id=event_id)
    participants = event.participants.all()
    qtd_participants = event.qtd_participants
    is_organizer = user_is_organizer(request, event, message=False)
    return render(request, 'participantes.html', {'participants': participants, 'event': event ,'user_is_organizer': is_organizer, 'qtd_participants': qtd_participants})

@login_required
def remover_participante(request, event_id, participant_id):
    event = Event.objects.get(id=event_id)
    
    if not user_is_organizer(request, event):
        return redirect('participantes', args=[event_id])
    elif event.has_passed():
        messages.add_message(request, constants.ERROR, f'Não é possível remover usuários do evento "{event.title}", pois ele já passou.')
        return redirect('organizando')

    else:
        if event.remove_user(participant_id):
            messages.add_message(request, constants.SUCCESS, 'Usuário removido com sucesso.')
        else:
            messages.add_message(request, constants.SUCCESS, f'Algo deu errado ao tentar remover esse usuário do evento {event.title}, pois ele já passou.')
        return redirect(reverse('participantes', args=[event_id]))

 
# Views de Participando 
@login_required
def participar(request, id_event):
    user = request.user

    event = Event.objects.get(id=id_event)
    redirect_event_details = reverse('ver_mais', args=[id_event])
    
    if event.has_passed():
        if event.private:
            messages.add_message(request, constants.ERROR, f'Não é possível solicitar partipação do evento "{event.title}", pois ele já passou.')
        else:
            messages.add_message(request, constants.ERROR, f'Não é possível participar do evento "{event.title}", pois ele já passou.')
        return redirect(redirect_event_details)

    if user.is_user_participant(event):
        messages.add_message(request, constants.ERROR, 'Você já participa deste evento.')
        return redirect(redirect_event_details)        

    if not event.free:
        if need_set_age(request, user):
            return redirect('perfil')
        
        elif user.is_minor():
            messages.add_message(request, constants.ERROR, 'Você não pode participar deste evento, pois ele é apenas para maiores de idade.')
            return redirect(redirect_event_details)
                
    if not event.private or user_is_organizer(request, event, message=False):
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
        solicitation_filter = request.GET.get('select_status_solicitation', 'w')
        events = Event.objects.filter(solicitation__user=user).filter(final_date_time__gte=datetime.now() - timedelta(days=1))
        events = events.annotate(status_solicitation=F('solicitation__status')).filter(status_solicitation=solicitation_filter)

    else:
        events = Event.objects.filter(participants=user).filter(final_date_time__gte=datetime.now() - timedelta(days=1))
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
def deixar_evento(request, event_id, render_solicitations=0):
    event = Event.objects.get(id=event_id)
    participando_url_redirect = reverse('participando', args=[render_solicitations])

    if render_solicitations == 1:
        if event.has_passed():
            messages.add_message(request, constants.ERROR, f'Não é possível remover a solicitação de um evento que já passou.')
        else:
            solicitation_ = event.solicitation_set.get(user=request.user)
            solicitation_.delete()
            messages.add_message(request, constants.SUCCESS, f'Solicitação de participação para o evento <b>{event.title} removida com sucessa</b>')  
    else:
        if event.has_passed():
            messages.add_message(request, constants.ERROR, f'Não é possível deixar de participar de um evento que já passou.')
        else:
            event.participants.remove(request.user)
            event.save()
            messages.add_message(request, constants.SUCCESS, f'Você <b>removeu</b> sua participação no evento <b>{event.title}</b>')
            
    return redirect(participando_url_redirect)


