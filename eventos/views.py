from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Event
from .forms import CreatEventForm

# Create your views here.
def organizando(request):
    return render(request, 'organizando.html')

def criar_evento(request):
    if request.method == "POST":
        form = CreatEventForm(request.POST)
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
        return redirect('organizando')
    else:
        form = CreatEventForm()
        return render(request, 'criar_evento.html', {'form': form})