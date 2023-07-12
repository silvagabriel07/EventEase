from django.urls import path
from . import views

urlpatterns = [
    path('organizando/', views.organizando, name='organizando'),
    path('organizando/criar_evento', views.criar_evento, name='criar_evento'),

]