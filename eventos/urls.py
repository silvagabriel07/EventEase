from django.urls import path
from . import views

urlpatterns = [
    path('organizar_eventos/', views.organizar_eventos, name='organizar_eventos'),
]