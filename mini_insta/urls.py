# File: models.py
# Author: Travis Falk(travisf@bu.edu), 9/25/2025
# Description: Model definitions for mini_insta app

from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
]