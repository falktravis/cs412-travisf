# File: admin.py
# Author: Travis Falk (travisf@bu.edu), 11/13/2025
# Description: Admin config for dadjokes app

from django.contrib import admin

from .models import Joke
from .models import Picture

# Register your models here.
admin.site.register(Joke)
admin.site.register(Picture)
