# File: views.py
# Author: Travis Falk(travisf@bu.edu), 10/2/2025
# Description: Form definitions for mini_insta app

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''Define a form to create a new post'''

    class Meta:
        model = Post
        fields = ['profile', 'timestamp', 'caption']