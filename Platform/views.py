from django.shortcuts import render
from eventos.models import Event, CATEGORIES
from datetime import datetime
from django.db.models import Count

# Create your views here.
def home(request):
    return render(request, 'home.html')

def explorar_eventos(request):
    categories = []
    for category in CATEGORIES:
        categories.append(category[0])

    search = request.GET.get('search')
    select_category = request.GET.get('select_category')
    select_num_participants = request.GET.get('select_num_participants')
    select_start_date_time = request.GET.get('select_start_date_time')
    private = request.GET.get('private')
    free = request.GET.get('free')
    
    events = Event.objects.all()
    if search:
        events = events.filter(title__icontains=search)
    if select_category:
        events = events.filter()

    if select_start_date_time:
        data_atual = datetime.now()
        if select_start_date_time == 'today':
            events = events.filter(start_date_time=data_atual)
        elif select_start_date_time == 'this_month':
            events = events.filter(start_date_time__month=data_atual.month)
        elif select_start_date_time == 'next_month':
            events = events.filter(start_date_time__month=data_atual.month + 1)
        elif select_start_date_time == 'this_year':
            events = events.filter(start_date_time__year=data_atual.year)
    if private:
        events = events.filter(private=True)
    if free:
        events = events.filter(free=True)

    if select_num_participants:
        if select_num_participants == 'gt_10':
            events = events.annotate(qtd_part=Count('participants')).filter(qtd_part__gt=10)
        elif select_num_participants == 'lt_10':
            events = events.annotate(qtd_part=Count('participants')).filter(qtd_part__lt=10)
        elif select_num_participants == 'gt_20':
            events = events.annotate(qtd_part=Count('participants')).filter(qtd_part__gt=20)
        elif select_num_participants == 'lt_20':
            events = events.annotate(qtd_part=Count('participants')).filter(qtd_part__lt=20)
        elif select_num_participants == 'gt_50':
            events = events.annotate(qtd_part=Count('participants')).filter(qtd_part__gt=50)
        elif select_num_participants == 'lt_50':
            events = events.annotate(qtd_part=Count('participants')).filter(qtd_part__lt=50)
        elif select_num_participants == 'gt_100':
            events = events.annotate(qtd_part=Count('participants')).filter(qtd_part__gt=100)
        elif select_num_participants == 'lt_100':
            events = events.annotate(qtd_part=Count('participants')).filter(qtd_part__lt=100)

        


    
        
    return render(request, 'explorar_eventos.html', {'events': events, 'categories': CATEGORIES})