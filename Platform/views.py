from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def explorar_eventos(request):
    return render(request, 'explorar_eventos.html')