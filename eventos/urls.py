from django.urls import path
from . import views

urlpatterns = [
    path('organizando/', views.organizando, name='organizando'),
    path('organizando/criar_evento/', views.criar_evento, name='criar_evento'),
    path('organizando/editar_event/<int:event_id>/', views.editar_evento, name='editar_evento'),
    path('organizando/remover_event_banner/<int:event_id>/', views.remover_event_banner, name='remover_event_banner'),
    path('organizando/<int:event_id>/excluir/', views.excluir_evento, name='excluir_evento'),
    path('organizando/solicitacoes_evento/<int:event_id>/', views.solicitacoes_evento, name='solicitacoes_evento'),
    path('organizando/solicitacoes_evento/<int:event_id>/rejeitar_solicitacao/<int:id_user_solicitation>/',views.rejeitar_solicitacao, name='rejeitar_solicitacao'),
    path('organizando/solicitacoes_evento/<int:event_id>/aceitar_solicitacao/<int:id_user_solicitation>/',views.aceitar_solicitacao, name='aceitar_solicitacao'),
    path('participando/<int:render_solicitations>/', views.participando, name='participando'),
    path('participando/sair/<int:event_id>/<int:render_solicitations>/', views.deixar_evento, name='deixar_evento'),
    path('ver_mais/<int:id_event>/', views.ver_mais, name='ver_mais'),
    path('ver_mais/<int:event_id>/participantes/', views.participantes, name='participantes'),
    path('ver_mais/<int:event_id>/participantes/remover_participante/<int:participant_id>/', views.remover_participante, name='remover_participante'),
    path('participar/<int:id_event>/', views.participar, name='participar'),
] 
