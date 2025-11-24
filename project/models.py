# File: models.py
# Author: Travis Falk(travisf@bu.edu), 11/24/2025
# Description: Model definitions for project app

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PropertyOwner(models.Model):
    """Store/represent property owner information."""
    name = models.TextField()
    is_company = models.BooleanField()
    
    def __str__(self):
        """Return a string representation of this model instance."""
        owner_type = "Company" if self.is_company else "Individual"
        return f'{self.name} ({owner_type})'


class UserProfile(models.Model):
    """Store/represent user profile information for the marketing list application."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    company = models.TextField()
    
    def __str__(self):
        """Return a string representation of this model instance."""
        return f'{self.first_name} {self.last_name} ({self.company})'


class Property(models.Model):
    """Store/represent property information for Massachusetts properties."""
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.TextField()
    zip_code = models.TextField()
    assessed_value = models.IntegerField()
    lat = models.FloatField()
    lon = models.FloatField()
    
    def __str__(self):
        """Return a string representation of this model instance."""
        return f'{self.address}, {self.city}, {self.zip_code}'


class List(models.Model):
    """Store/represent marketing lists created by users."""
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property)
    list_name = models.TextField()
    creation_date = models.DateField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        """Return a string representation of this model instance."""
        return f'{self.list_name} (created by {self.creator.first_name} {self.creator.last_name})'
