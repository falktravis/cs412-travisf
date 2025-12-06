# File: models.py
# Author: Travis Falk(travisf@bu.edu), 11/24/2025
# Description: Model definitions for project app

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from math import radians, cos, sin, asin, sqrt
import csv

# Create your views here.

class PropertyOwner(models.Model):
    """Store/represent property owner information."""
    name = models.TextField()
    address = models.TextField()
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
    
    def get_absolute_url(self):
        """Return URL to this profile (used after update)."""
        return reverse('show_profile')
    
    def get_all_lists(self):
        """Retrieve all lists created by this user profile as a QuerySet."""
        return List.objects.filter(creator=self).order_by('-creation_date')


class Property(models.Model):
    """Store/represent property information for Massachusetts properties."""
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.TextField()
    zip_code = models.TextField()
    assessed_value = models.IntegerField()
    style = models.TextField()
    year_built = models.IntegerField()
    lat = models.FloatField()
    lon = models.FloatField()
    
    def __str__(self):
        """Return a string representation of this model instance."""
        return f'{self.address}, {self.city}, {self.zip_code}'
    
    def get_absolute_url(self):
        """Return URL to this property detail page."""
        return reverse('show_property', kwargs={'pk': self.pk})


class List(models.Model):
    """Store/represent marketing lists created by users."""
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property)
    list_name = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    center_address = models.TextField(blank=True)
    center_lat = models.FloatField(default=0, blank=True)
    center_lon = models.FloatField(default=0, blank=True)
    radius_miles = models.FloatField(default=0, blank=True)
    
    def __str__(self):
        """Return a string representation of this model instance."""
        return f'{self.list_name} (created by {self.creator.first_name} {self.creator.last_name})'
    
    def get_absolute_url(self):
        """Return URL to this list detail page."""
        return reverse('show_list', kwargs={'pk': self.pk})
    
    def get_property_count(self):
        """Return the count of properties in this list."""
        return self.properties.count()
    
    def get_total_assessed_value(self):
        """Return the total assessed value of all properties in this list."""
        total = sum(prop.assessed_value for prop in self.properties.all())
        return total
    
import os
from django.conf import settings

def load_data():
    """
    Load property data from CSV file into the database.
    Hardcoded to look for parcels.csv in the project root directory.
    
    Returns:
        Dictionary with counts of created records
    """
    
    # Hardcoded file path - adjust this to match your file location
    file_path = os.path.join(settings.BASE_DIR, 'properties.csv')
    
    # Delete existing property and owner data to start fresh
    Property.objects.all().delete()
    PropertyOwner.objects.all().delete()
    
    # Track statistics
    owners_created = 0
    properties_created = 0
    
    # Cache for owners to avoid duplicate lookups
    owner_cache = {}
    
    print(f"Loading data from {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, start=1):
            # Extract and validate required fields
            owner_name = row.get('OWNER1', '').strip()
            owner_address = row.get('OWN_ADDR', '').strip() + ", " + row.get('OWN_CITY', '').strip() + ", " + row.get('OWN_STATE', '').strip() + " " + row.get('OWN_ZIP', '').strip()
            address = row.get('ADDR_NUM', '').strip() + " " + row.get('FULL_STR', '').strip()
            city = row.get('CITY', '').strip()
            zip_code = row.get('ZIP', '').strip()
            lat_str = row.get('lat', '').strip()
            lon_str = row.get('lon', '').strip()
            total_val_str = row.get('TOTAL_VAL', '').strip()
            style = row.get('STYLE', '').strip()
            year_built_str = row.get('YEAR_BUILT', '').strip()
            
            # Parse numeric values
            try:
                lat = float(lat_str)
                lon = float(lon_str)
                total_value = int(float(total_val_str))
                year_built = int(year_built_str)
            except (ValueError, TypeError):
                continue
            
            # Skip properties with invalid coordinates or zero value
            if lat == 0 or lon == 0:
                continue
            
            # Ensure ZIP code is valid (5 digits)
            if zip_code:
                zip_code = zip_code[:5]
            else:
                zip_code = '00000'
            
            # Determine if owner is a company or individual
            # Common indicators: LLC, INC, CORP, TRUST, REALTY, etc.
            company_keywords = ['LLC', 'INC', 'CORP', 'CORPORATION', 'TRUST', 
                                'REALTY', 'PROPERTIES', 'COMPANY', 'CO ', 'LTD',
                                'PARTNERSHIP', 'LP', 'ASSOCIATES']
            is_company = any(keyword in owner_name.upper() for keyword in company_keywords)
            
            # Get or create PropertyOwner
            owner_key = (owner_name, owner_address, is_company)
            if owner_key in owner_cache:
                owner = owner_cache[owner_key]
            else:
                owner, created = PropertyOwner.objects.get_or_create(
                    name=owner_name,
                    address=owner_address,
                    is_company=is_company
                )
                owner_cache[owner_key] = owner
                if created:
                    owners_created += 1
            
            # Create Property
            Property.objects.create(
                owner=owner,
                address=address,
                city=city,
                zip_code=zip_code,
                assessed_value=total_value,
                style=style,
                year_built=year_built,
                lat=lat,
                lon=lon
            )
            
            # Print progress every 1000 rows
            if row_num % 1000 == 0:
                print(f"  Processed {row_num} rows... ({properties_created} properties, {owners_created} owners)")
    
    # Print final statistics
    print(f"Property Owners Created: {owners_created}")
    print(f"Properties Created: {properties_created}")
    
    return {
        'owners_created': owners_created,
        'properties_created': properties_created
    }
