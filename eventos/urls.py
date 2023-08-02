from django.urls import path
from . import views

urlpatterns = [
    path('organizando/<int:user_id>/', views.organizando, name='organizando'),
    path('organizando/criar_evento/', views.criar_evento, name='criar_evento'),
    path('organizando/<int:user_id>/editar_event/<int:event_id>/', views.editar_evento, name='editar_evento'),
    path('organizando/<int:user_id>/solicitacoes_evento/<int:event_id>/', views.solicitacoes_evento, name='solicitacoes_evento'),
    path('organizando/<int:user_id>/solicitacoes_evento/<int:event_id>/rejeitar_solicitacao/<int:id_solicitation>/',views.rejeitar_solicitacao, name='rejeitar_solicitacao'),
    path('organizando/<int:user_id>/solicitacoes_evento/<int:event_id>/aceitar_solicitacao/<int:id_solicitation>/',views.aceitar_solicitacao, name='aceitar_solicitacao'),
    path('participando/<int:user_id>/<int:render_solicitations>/', views.participando, name='participando'),
    path('participando/solicitacoes/<int:user_id>/', views.participando_solicitacoes, name='participando_solicitacoes'),
    path('participando/sair/<int:event_id>/<int:render_solicitations>/', views.leave_event, name='leave_event'),
    path('ver_mais/<int:id_event>/', views.ver_mais, name='ver_mais'),
    path('participar/<int:id_event>/', views.participar, name='participar'),
] 
