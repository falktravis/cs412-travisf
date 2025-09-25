# File: urls.py
# Author: Travis Falk(travisf@bu.edu), 9/9/2025
# Description: Url definitions for quotes app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.quote, name='quote_home'),
    path('quote/', views.quote, name='quote'),
    path('show_all/', views.show_all, name='show_all'),
    path('about/', views.about, name='about'),
]