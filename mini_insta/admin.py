# File: admin.py
# Author: Travis Falk(travisf@bu.edu), 9/25/2025
# Description: Admin config for mini_insta app

from django.contrib import admin

from .models import Profile
from .models import Post
from .models import Photo
from .models import Follow
from .models import Comment
from .models import Like

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)
