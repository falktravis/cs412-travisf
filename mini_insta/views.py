# File: views.py
# Author: Travis Falk(travisf@bu.edu), 9/25/2025
# Description: View definitions for mini_insta app

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile


# Create your views here.
class ProfileListView(ListView):
    '''Define a view to list all profiles'''

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Define a view to show profile details'''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'