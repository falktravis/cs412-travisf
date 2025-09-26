# File: admin.py
# Author: Travis Falk(travisf@bu.edu), 9/25/2025
# Description: Admin config for mini_insta app

from django.contrib import admin

from .models import Profile

# Register your models here.
admin.site.register(Profile)