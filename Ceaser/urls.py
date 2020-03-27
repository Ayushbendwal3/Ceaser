from django.contrib import admin
from django.urls import path
from Ceaser import views

urlpatterns = [
    path('', views.index, name=''),
    path('upload', views.upload, name='upload'),
    path('index', views.index, name='index'),
    path('home', views.home, name='home'),
    path('user_login', views.user_login, name='login'),
    path('register', views.register, name='registers'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('special', views.special, name='special'),
]