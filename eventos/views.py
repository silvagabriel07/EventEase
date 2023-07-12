from django.shortcuts import render

# Create your views here.
def organizando(request):
    return render(request, 'organizando.html')

def criar_evento(request):
    return render(request, 'criar_evento.html')