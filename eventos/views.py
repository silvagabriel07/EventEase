from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Event
from .forms import CreatEventForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def organizando(request, user_id):
    if not request.user.id == user_id:
        return HttpResponse('Os eventos que você deseja visualizar não são seus.')
    my_events = Event.objects.filter(organizer=user_id)
    for event in my_events:
        print(event.category)
        for category in event.category:
            print(category)
    return render(request, 'organizando.html', {'my_events': my_events})

@login_required
def criar_evento(request):
    if request.method == "POST":
        form = CreatEventForm(request.POST, request.FILES)
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
                category=category,
                private=private,
                free=free,
                start_date_time=start_date_time,
                final_date_time=final_date_time,
                event_banner=event_banner,
                organizer=organizer,
            )
            event.save()
            redirect_url = reverse('organizando', args=[organizer.id])
            return redirect(redirect_url)
            
    else:
        form = CreatEventForm()
        return render(request, 'criar_evento.html', {'form': form})
    
