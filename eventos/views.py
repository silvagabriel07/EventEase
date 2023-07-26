from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Event
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
        return HttpResponse('Os eventos que você deseja visualizar não são seus.')
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

            print(category.id)

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
    
    if need_set_age(request, user):
        return redirect('profile')

    event = Event.objects.get(id=id_event)
    redirect_event_details = reverse('ver_mais', args=[id_event])

    if user.is_user_participant(event):
        messages.add_message(request, constants.ERROR, 'Você já participa deste evento.')
    
    elif not event.free:
        need_set_age(request, user)
        if user.is_minor():
            messages.add_message(request, constants.ERROR, 'Você não pode participar deste evento, pois ele é apenas para maiores de idade.')

    else:
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

