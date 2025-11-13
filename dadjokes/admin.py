from django.contrib import admin

from .models import Joke
from .models import Picture

# Register your models here.
admin.site.register(Joke)
admin.site.register(Picture)
