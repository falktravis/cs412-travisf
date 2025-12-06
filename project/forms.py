# File: forms.py
# Author: Travis Falk(travisf@bu.edu), 12/2/2025
# Description: Form definitions for project app

from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):
    """Form to create a new profile."""

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'company']


class UpdateProfileForm(forms.ModelForm):
    """Form to update a profile."""

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'company']


class CreateListForm(forms.ModelForm):
    """Form to create a new list."""

    class Meta:
        model = List
        fields = ['list_name', 'notes', 'center_address', 'radius_miles']


class CreateListMapForm(forms.ModelForm):
    """Form to create a new list via map interface."""

    class Meta:
        model = List
        fields = ['list_name', 'notes', 'radius_miles', 'center_lat', 'center_lon']