# File: models.py
# Author: Travis Falk(travisf@bu.edu), 9/25/2025
# Description: Model definitions for mini_insta app


from django.db import models

# Create your models here.
class Profile(models.Model):
    """Profile model to store user profile information."""
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_name} (@{self.username})"