from django.shortcuts import render
from eventos.models import Event, Category
from datetime import datetime
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    return render(request, 'home.html')

def explorar_eventos(request):
    search = request.GET.get('search', '')
    select_category = request.GET.get('select_category')
    select_num_participants = request.GET.get('select_num_participants')
    select_start_date_time = request.GET.get('select_start_date_time')
    select_private = request.GET.get('select_private')
    select_free = request.GET.get('select_free')

    events = Event.objects.all()
    categories = Category.objects.all()
    
    if search:
        events = events.filter(title__icontains=search)
    
    if select_category:
        events = events.filter(category_id=select_category)

    if select_start_date_time:
        data_atual = datetime.now()
        if select_start_date_time == 'today':
            events = events.filter(start_date_time__year=data_atual.year).filter(start_date_time__month=data_atual.month).filter(start_date_time__day=data_atual.day)
        elif select_start_date_time == 'this_month':
            events = events.filter(start_date_time__month=data_atual.month)
        elif select_start_date_time == 'next_month':
            events = events.filter(start_date_time__month=data_atual.month + 1)
        elif select_start_date_time == 'this_year':
            events = events.filter(start_date_time__year=data_atual.year)

    if select_private:
        if select_private == "true":
            events = events.filter(private=True)
        elif select_private == "false":
            events = events.filter(private=False)

    if select_free:
        if select_free == "true":
            events = events.filter(free=True)
        elif select_free == "false":
            events = events.filter(free=False)

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
        
    page_num = request.GET.get('page', '1')
    event_paginator = Paginator(events, 4)
    try:
        page = event_paginator.page(page_num)
    except(EmptyPage, PageNotAnInteger):
        page = event_paginator.page(1)
    
    return render(request, 'explorar_eventos.html', {'page': page, 'categories':  categories})

