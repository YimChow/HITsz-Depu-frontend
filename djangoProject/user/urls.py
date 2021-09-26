from django.urls import path
from .views import *
urlpatterns = [
    path('login', loginView, name='login'),
    path('register', registerView, name='register'),
    path('setps', setpsView, name='setps'),
    path('logout', logoutView, name='logout'),
]
