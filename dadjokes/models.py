# File: models.py
# Author: Travis Falk (travisf@bu.edu), 11/13/2025
# Description: Model definitions for dadjokes app

from django.db import models

# Create your models here.

class Joke(models.Model):
    """Model representing a dad joke."""
    text = models.TextField(blank=True)
    contributor = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """String representation of the joke."""
        return f"{self.text[:50]}... - by {self.contributor}"


class Picture(models.Model):
    """Model representing a silly picture or GIF."""
    image_url = models.URLField(blank=True)
    contributor = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """String representation of the picture."""
        return f"Picture by {self.contributor} - {self.image_url[:50]}..."
