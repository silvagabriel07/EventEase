from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Event
from .forms import CreateEventForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants

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
    
