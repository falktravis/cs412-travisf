# File: urls.py
# Author: Travis Falk(travisf@bu.edu), 9/17/2025
# Description: Url definitions for restaurant app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.main, name='restaurant_home'),
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]