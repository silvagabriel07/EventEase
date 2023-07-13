from django.shortcuts import render
from eventos.models import Event

# Create your views here.
def home(request):
    return render(request, 'home.html')

def explorar_eventos(request):
    events = Event.objects.all()
    return render(request, 'explorar_eventos.html', {'events': events})