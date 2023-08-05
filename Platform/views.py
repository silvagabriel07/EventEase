from django.shortcuts import render, redirect
from eventos.models import Event, Category
from datetime import datetime, timedelta
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ProfileForm, PhoneNumberForm
from django import forms
from account_manager.models import User, PhoneNumber
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    num_featured_events = 6
    featured_events = Event.objects.all().annotate(qtd_part=Count('participants')).order_by('-qtd_part')[:num_featured_events]
    for event in featured_events: print(event.qtd_participants)
    return render(request, 'home.html', {'events': featured_events})


def explorar_eventos(request):
    search = request.GET.get('search', '')
    select_category = request.GET.get('select_category')
    select_num_participants = request.GET.get('select_num_participants')
    select_start_date_time = request.GET.get('select_start_date_time')
    select_private = request.GET.get('select_private')
    select_free = request.GET.get('select_free')
    data_atual = datetime.now()
    # para pegar os eventos que já acabaram, com excessão se só se passou um dia depois de sua finalização
    events = Event.objects.filter(final_date_time__gte=data_atual - timedelta(days=1))
    categories = Category.objects.all()
    
    if search:
        events = events.filter(title__icontains=search)
    
    if select_category:
        events = events.filter(category_id=select_category)

    if select_start_date_time:
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
    event_paginator = Paginator(events, 24)
    try:
        page = event_paginator.page(page_num)
    except(EmptyPage, PageNotAnInteger):
        page = event_paginator.page(1)
    
    return render(request, 'explorar_eventos.html', {'page': page, 'categories':  categories, 'value_select_category': select_category})


@login_required
def perfil(request):
    user_img = request.user.user_img
    if request.method == 'GET':
        phone_numbers = request.user.phonenumber_set.all()
        extra = 0
        for ex in range(3, -1, -1):
            if phone_numbers.count() == ex:
                extra = 3 - ex 

        form_factory = forms.inlineformset_factory(User, PhoneNumber, form=PhoneNumberForm, extra=extra)

        form_filho = form_factory(instance=request.user)
        form = ProfileForm(instance=request.user)
        return render(request, 'perfil.html', {'form': form, 'form_filho': form_filho, 'user_img': user_img})
    elif request.method == 'POST':
        form_factory = forms.inlineformset_factory(User, PhoneNumber, form=PhoneNumberForm)
        form_filho = form_factory(request.POST, instance=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid() and form_filho.is_valid():
            formulario = form.save()
            form_filho.instance = formulario
            form_filho.save()
            messages.add_message(request, constants.SUCCESS, 'Alterações salvas.')
            return redirect('perfil')
        else:
            return render(request, 'perfil.html', {'form': form, 'form_filho': form_filho, 'user_img': user_img})

        
def ver_perfil(request, user_id):
    user = User.objects.get(id=user_id)
    qtd_events_organizing = Event.objects.filter(organizer=user).count()
    qtd_event_participanting = user.event_participants.all().count()
    return render(request, 'ver_perfil.html', {'user': user, 'qtd_events_organizing': qtd_events_organizing, 'qtd_event_participanting': qtd_event_participanting})


def ver_eventos_participando(request, user_id):
    user = User.objects.get(id=user_id)
    event_participanting = user.event_participants.filter(final_date_time__gte=datetime.now() - timedelta(days=1))
    return render(request, 'ver_eventos_participando.html', {'user': user, 'event_participanting': event_participanting})


def ver_eventos_organizando(request, user_id):
    user = User.objects.get(id=user_id)
    events_organizing = Event.objects.filter(organizer=user).filter(final_date_time__gte=datetime.now() - timedelta(days=1))
    return render(request, 'ver_eventos_organizando.html', {'user': user, 'events_organizing': events_organizing})