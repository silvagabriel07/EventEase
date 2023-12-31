from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('explorar_eventos/', views.explorar_eventos, name='explorar_eventos'),
    path('perfil/', views.perfil, name='perfil'),
    path('ver_perfil/<int:user_id>/', views.ver_perfil, name='ver_perfil'),
    path('ver_eventos_participando/<int:user_id>/', views.ver_eventos_participando, name='ver_eventos_participando'),
    path('ver_eventos_organizando/<int:user_id>/', views.ver_eventos_organizando, name='ver_eventos_organizando'),
    re_path('notificacoes/', include('notifications.urls', namespace='notifications')),

]