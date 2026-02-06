from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Chat
    path('', views.index, name='index'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('room/<str:room_name>/send/', views.send_message, name='send_message'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
]