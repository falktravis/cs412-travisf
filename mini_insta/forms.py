# File: forms.py
# Author: Travis Falk(travisf@bu.edu), 10/2/2025
# Description: Form definitions for mini_insta app

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''Define a form to create a new post'''

    class Meta:
        model = Post
        fields = ['caption']


class UpdateProfileForm(forms.ModelForm):
    '''Form to update a profile (not username or join_date).'''

    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']


class UpdatePostForm(forms.ModelForm):
    '''Update a Post (caption only).'''

    class Meta:
        model = Post
        fields = ['caption']


class CreateProfileForm(forms.ModelForm):
    '''Form to create a new profile.'''

    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'profile_image_url', 'bio_text']