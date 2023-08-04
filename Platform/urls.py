from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('explorar_eventos/', views.explorar_eventos, name='explorar_eventos'),
    path('profile/', views.profile, name='profile'),
    path('view_profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('view_participating_events/<int:user_id>/', views.view_participating_events, name='view_participating_events'),
    path('view_organizing_events/<int:user_id>/', views.view_organizing_events, name='view_organizing_events'),
]