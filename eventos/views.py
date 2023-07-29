from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Event
from django.db.models import Count
from .forms import CreateEventForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Solicitation
from account_manager.utils import need_set_age
from account_manager.utils import need_set_age

# Create your views here.
@login_required
def organizando(request, user_id):
    if not request.user.id == user_id:
        messages.add_message(request, constants.ERROR, 'Algo deu errado.')
        return redirect('home')
    my_events = Event.objects.filter(organizer=user_id)
    return render(request, 'organizando.html', {'my_events': my_events})

@login_required
def criar_evento(request):
    if request.method == "POST":
        form = CreateEventForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            private = form.cleaned_data['private']
            free = form.cleaned_data['free']
            start_date_time = form.cleaned_data['start_date_time']
            final_date_time = form.cleaned_data['final_date_time']
            event_banner = form.cleaned_data['event_banner']

            organizer = request.user

            event = Event(
                title=title,
                description=description,
                category_id=category.id,
                private=private,
                free=free,
                start_date_time=start_date_time,
                final_date_time=final_date_time,
                event_banner=event_banner,
                organizer=organizer,
            )
            event.save()
            messages.add_message(request, constants.SUCCESS, 'Evento criado com sucesso.')
            redirect_url = reverse('organizando', args=[organizer.id])
            return redirect(redirect_url)
        else:
            return render(request, 'criar_evento.html', {'form': form})
    else:
        form = CreateEventForm()
        return render(request, 'criar_evento.html', {'form': form})

def ver_mais(request, id_event):
    event = Event.objects.get(id=id_event)
    is_user_participant = False
    user_already_solicitated = False
    if request.user.is_authenticated:
        is_user_participant = request.user.is_user_participant(event)
        user_already_solicitated = request.user.user_already_solicitated(event)
    return render(request, 'ver_mais.html', {'event': event, 'is_user_participant': is_user_participant, 'user_already_solicitated': user_already_solicitated})

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
                
    if not event.private:
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
def participando(request, user_id, render_solicitations=0):
    user = request.user
    if not user.id == user_id:
        messages.add_message(request, constants.ERROR, 'Algo deu errado.')
        return redirect('home')
    
    if render_solicitations == 1:
        events = Event.objects.filter(solicitation__user=user)
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


def participando_solicitacoes(request, user_id):
    render_solicitations = 1
    participando_url_redirect = reverse('participando', args=[user_id, render_solicitations])
    return redirect(participando_url_redirect)

def leave_event(request, event_id, render_solicitations=0):
    event = Event.objects.get(id=event_id)

    if render_solicitations == 1:
        solicitation_ = event.solicitation_set.get(user=request.user)
        solicitation_.delete()
        messages.add_message(request, constants.SUCCESS, f'Solicitação de participação para o evento <b>{event.title} removida com sucessa</b>')  
    else:
        event.participants.remove(request.user)
        event.save()
        messages.add_message(request, constants.SUCCESS, f'Você <b>removeu</b> sua participação no evento <b>{event.title}</b>')
    return redirect(reverse('participando', args=[request.user.id, render_solicitations]))
