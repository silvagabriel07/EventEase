from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('explorar_eventos/', views.explorar_eventos, name='explorar_eventos'),
    path('profile/', views.profile, name='profile')
]