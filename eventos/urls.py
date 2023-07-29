from django.urls import path
from . import views

urlpatterns = [
    path('organizando/<int:user_id>/', views.organizando, name='organizando'),
    path('organizando/criar_evento/', views.criar_evento, name='criar_evento'),
    path('participando/<int:user_id>/<int:render_solicitations>/', views.participando, name='participando'),
    path('participando/solicitacoes/<int:user_id>/', views.participando_solicitacoes, name='participando_solicitacoes'),
    path('ver_mais/<int:id_event>/', views.ver_mais, name='ver_mais'),
    path('participar/<int:id_event>/', views.participar, name='participar'),
] 
