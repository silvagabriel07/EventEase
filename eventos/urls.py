from django.urls import path
from . import views

urlpatterns = [
    path('organizando/', views.organizando, name='organizando'),
]