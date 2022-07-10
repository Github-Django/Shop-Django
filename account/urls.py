from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views

app_name = 'account'
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/address/', AddressView.as_view(), name='address'),
    path('profile/history/', history, name='history'),
    path('profile/view_count/', view_count, name='view_count'),
]
