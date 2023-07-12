from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Event
from .forms import CreatEventForm

# Create your views here.
def organizando(request):
    return render(request, 'organizando.html')

def criar_evento(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        categories = request.POST.getlist('categories[]')
        free = request.POST.get('free')
        private = request.POST.get('private')
        start_date_time = request.POST.get('start_date_time')
        last_date_time = request.POST.get('last_date_time')
        banner_event = request.FILES.get('banner_event')

        # VALIDATIONS

        event = Event(
            title=title,
            description=description,
            categories=categories,
            free=free,
            private=private,
            start_date_time=start_date_time,
            last_date_time=last_date_time,
            banner_event=banner_event
        )
        event.save()
        return redirect('organizando')
    else:
        form = CreatEventForm()
        return render(request, 'criar_evento.html', {'form': form})