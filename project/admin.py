# File: admin.py
# Author: Travis Falk(travisf@bu.edu), 11/24/2025
# Description: Admin config for project app

from django.contrib import admin

from .models import PropertyOwner
from .models import UserProfile
from .models import Property
from .models import List

# Register your models here.
admin.site.register(PropertyOwner)
admin.site.register(UserProfile)
admin.site.register(Property)
admin.site.register(List)
