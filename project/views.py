# File: views.py
# Author: Travis Falk(travisf@bu.edu), 12/2/2025
# Description: View definitions for project app

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.shortcuts import render, redirect
from .models import UserProfile, Property, PropertyOwner, List
from .forms import CreateProfileForm, UpdateProfileForm, CreateListForm, CreateListMapForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
import csv
from math import radians, cos, sin, asin, sqrt


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on earth (in miles)."""
    # Source: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in miles
    r = 3956
    
    return c * r


def geocode_address(address):
    """Convert an address to latitude and longitude using our local database."""
    # Search for a property with a matching address in our database
    # Use icontains to allow for partial matches ("123 Main" matches "123 Main St")
    property = Property.objects.filter(address__icontains=address).first()
    
    if property:
        return property.lat, property.lon
    else:
        return None, None


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Custom mixin to require login and provide helper methods."""
    
    def get_login_url(self) -> str:
        """Return the URL required for login."""
        return reverse('login')
    
    def get_profile(self):
        """Return the UserProfile for the logged in user."""
        return UserProfile.objects.get(user=self.request.user)


class PropertyListView(CustomLoginRequiredMixin, ListView):
    """Define a view to list all properties."""
    
    model = Property
    template_name = 'project/show_all_properties.html'
    context_object_name = 'properties'
    paginate_by = 50
    
    def get_queryset(self):
        """Return the QuerySet of properties, optionally filtered."""
        queryset = Property.objects.all()
        
        # Check for filter parameters
        search_query = self.request.GET.get('search')
        city = self.request.GET.get('city')
        zip_code = self.request.GET.get('zip_code')
        min_value = self.request.GET.get('min_value')
        max_value = self.request.GET.get('max_value')
        
        # Apply filters if present
        if search_query:
            queryset = queryset.filter(address__icontains=search_query)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if zip_code:
            queryset = queryset.filter(zip_code__icontains=zip_code)
        if min_value:
            queryset = queryset.filter(assessed_value__gte=min_value)
        if max_value:
            queryset = queryset.filter(assessed_value__lte=max_value)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add viewer_profile and filter parameters for navbar links when authenticated."""
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context['viewer_profile'] = profile
        
        # Add filter parameters to context for form persistence
        context['search_filter'] = self.request.GET.get('search', '')
        context['city_filter'] = self.request.GET.get('city', '')
        context['zip_filter'] = self.request.GET.get('zip_code', '')
        context['min_value_filter'] = self.request.GET.get('min_value', '')
        context['max_value_filter'] = self.request.GET.get('max_value', '')
        
        # Get unique cities and zip codes for filter dropdowns
        context['cities'] = Property.objects.values_list('city', flat=True).distinct().order_by('city')
        context['zip_codes'] = Property.objects.values_list('zip_code', flat=True).distinct().order_by('zip_code')
        
        return context


class PropertyDetailView(CustomLoginRequiredMixin, DetailView):
    """Define a view to show property details."""
    
    model = Property
    template_name = 'project/show_property.html'
    context_object_name = 'property'
    
    def get_context_data(self, **kwargs):
        """Add viewer_profile for navbar links when authenticated."""
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context['viewer_profile'] = profile
        return context


class ListListView(CustomLoginRequiredMixin, ListView):
    """Define a view to list all lists for the logged in user."""
    
    template_name = 'project/show_all_lists.html'
    context_object_name = 'lists'
    
    def get_queryset(self):
        """Return the QuerySet of lists for the logged in user."""
        profile = self.get_profile()
        return profile.get_all_lists()
    
    def get_context_data(self, **kwargs):
        """Add the profile to the context data."""
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context['profile'] = profile
        context['viewer_profile'] = profile
        return context


class ListDetailView(CustomLoginRequiredMixin, DetailView):
    """Define a view to show list details."""
    
    model = List
    template_name = 'project/show_list.html'
    context_object_name = 'list'
    
    def get_context_data(self, **kwargs):
        """Add viewer_profile for navbar links when authenticated."""
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context['viewer_profile'] = profile
        
        # Add pagination for properties
        properties_list = self.object.properties.all()
        paginator = Paginator(properties_list, 50) # Show 50 properties per page
        
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['page_obj'] = page_obj
        context['properties'] = page_obj
        
        return context


class ShowProfileView(CustomLoginRequiredMixin, TemplateView):
    """Define a view to show the user's profile dashboard."""
    
    template_name = 'project/show_profile.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Check if user has a profile, redirect to creation if not."""
        # Let the LoginRequiredMixin handle authentication first
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
        # Now check if authenticated user has a profile
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return redirect('create_profile')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Add profile and lists to the context data."""
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context['profile'] = profile
        context['viewer_profile'] = profile
        context['lists'] = profile.get_all_lists()
        return context

class CreateProfileView(CreateView):
    """Define a view to create a new user profile."""
    
    form_class = CreateProfileForm
    template_name = 'project/create_profile_form.html'
    
    def get_success_url(self):
        """Return URL to redirect to after successful profile creation."""
        return reverse('show_profile')
    
    def get_context_data(self, **kwargs):
        """Add UserCreationForm to context data."""
        
        # Call the superclass method
        context = super().get_context_data(**kwargs)
        
        # Create an instance of UserCreationForm and add to context
        context['user_form'] = UserCreationForm()
        
        return context
    
    def form_valid(self, form):
        """Handle form submission: create User and Profile."""
        
        # Reconstruct the UserCreationForm from POST data
        user_form = UserCreationForm(self.request.POST)
        
        # Save the User object
        user = user_form.save()
        
        # Log the user in
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Attach the User to the Profile instance
        form.instance.user = user
        
        # Delegate to superclass to save the Profile
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        """Handle the request and redirect if user already has a profile."""
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                return redirect('show_profile')
            except UserProfile.DoesNotExist:
                pass
        return super().dispatch(request, *args, **kwargs)


class UpdateProfileView(CustomLoginRequiredMixin, UpdateView):
    """Define a view to update a user profile."""
    
    model = UserProfile
    form_class = UpdateProfileForm
    template_name = 'project/update_profile_form.html'
    
    def get_object(self):
        """Return the UserProfile object for the logged in user."""
        return self.get_profile()
    
    def get_context_data(self, **kwargs):
        """Add viewer_profile for navbar links when authenticated."""
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context['profile'] = profile
        context['viewer_profile'] = profile
        return context


class CreateListView(CustomLoginRequiredMixin, CreateView):
    """Define a view to create a new list."""
    
    form_class = CreateListForm
    template_name = 'project/create_list_form.html'
    
    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""
        
        # Calling the superclass method
        context = super().get_context_data(**kwargs)
        
        # Get profile from logged in user
        profile = self.get_profile()
        
        # Add this profile into the context dictionary
        context['profile'] = profile
        context['viewer_profile'] = profile
        return context
    
    def form_valid(self, form):
        """This method handles the form submission and saves the new object to the Django database."""
        
        # Get profile from logged in user
        profile = self.get_profile()
        
        # Attach this profile to the list
        form.instance.creator = profile
        
        # Get the center address and radius from the form
        center_address = form.cleaned_data.get('center_address')
        radius_miles = form.cleaned_data.get('radius_miles')
        
        # Geocode the address to get lat/lon
        if center_address and radius_miles:
            lat, lon = geocode_address(center_address)
            
            if lat is not None and lon is not None:
                # Store the geocoded coordinates
                form.instance.center_lat = lat
                form.instance.center_lon = lon
                
                # Save the list first
                response = super().form_valid(form)
                
                # Find properties within radius
                # USing bounding boxes to make this faster instead of checking every single property
                # 1 degree of latitude is about 69 miles
                # 1 degree of longitude is about 50 miles
                lat_delta = radius_miles / 69.0
                lon_delta = radius_miles / 50.0
                
                # First get a smaller list of properties that are roughly close by
                nearby_properties = Property.objects.filter(
                    lat__gte=lat - lat_delta,
                    lat__lte=lat + lat_delta,
                    lon__gte=lon - lon_delta,
                    lon__lte=lon + lon_delta
                )
                
                # Then check the exact distance for each one
                for prop in nearby_properties:
                    distance = haversine_distance(lat, lon, prop.lat, prop.lon)
                    if distance <= radius_miles:
                        self.object.properties.add(prop)
                
                return response
            else:
                # If geocoding fails, still save but without properties
                return super().form_valid(form)
        else:
            # No address/radius provided, just save the list
            return super().form_valid(form)


class UpdateListView(CustomLoginRequiredMixin, UpdateView):
    """Define a view to update a list."""
    
    model = List
    
    def get_form_class(self):
        """Return the appropriate form class based on list type."""
        if self.object.center_address:
            return CreateListForm
        else:
            return CreateListMapForm
            
    def get_template_names(self):
        """Return the appropriate template based on list type."""
        if self.object.center_address:
            return ['project/update_list_form.html']
        else:
            return ['project/update_list_map.html']
    
    def get_queryset(self):
        """Restrict updates to lists owned by the logged-in user."""
        return List.objects.filter(creator__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """Add viewer_profile for navbar links when authenticated."""
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context['viewer_profile'] = profile
        return context
    
    def form_valid(self, form):
        """Handle form submission and recalculate properties if address/radius changed."""
        
        # Check if this is a map-based list (blank address)
        if not self.object.center_address:
            # Map-based update logic
            response = super().form_valid(form)
            
            # Get updated values
            center_lat = self.object.center_lat
            center_lon = self.object.center_lon
            radius_miles = self.object.radius_miles
            
            # Clear existing properties
            self.object.properties.clear()
            
            # Find properties within radius
            # Using the same bounding box logic as in CreateListView
            lat_delta = radius_miles / 69.0
            lon_delta = radius_miles / 50.0
            
            nearby_properties = Property.objects.filter(
                lat__gte=center_lat - lat_delta,
                lat__lte=center_lat + lat_delta,
                lon__gte=center_lon - lon_delta,
                lon__lte=center_lon + lon_delta
            )
            
            # Calculate exact distances and add properties within radius
            for prop in nearby_properties:
                distance = haversine_distance(center_lat, center_lon, prop.lat, prop.lon)
                if distance <= radius_miles:
                    self.object.properties.add(prop)
            
            return response
            
        else:
            # Address-based update logic
            # Get the center address and radius from the form
            center_address = form.cleaned_data.get('center_address')
            radius_miles = form.cleaned_data.get('radius_miles')
            
            # Check if address or radius changed
            # Note: self.object is already updated by super().form_valid(form) if we call it first
            # But we need to compare with old values.
            # However, UpdateView updates the object in form_valid.
            
            # Let's check changed data from form.changed_data
            if 'center_address' in form.changed_data or 'radius_miles' in form.changed_data:
                if center_address and radius_miles:
                    # Geocode the address to get lat/lon
                    lat, lon = geocode_address(center_address)
                    
                    if lat is not None and lon is not None:
                        # Store the geocoded coordinates
                        form.instance.center_lat = lat
                        form.instance.center_lon = lon
                        
                        # Save the list first
                        response = super().form_valid(form)
                        
                        # Clear existing properties and recalculate
                        self.object.properties.clear()
                        
                        # Find properties within radius
                        lat_delta = radius_miles / 69.0
                        lon_delta = radius_miles / 50.0
                        
                        nearby_properties = Property.objects.filter(
                            lat__gte=lat - lat_delta,
                            lat__lte=lat + lat_delta,
                            lon__gte=lon - lon_delta,
                            lon__lte=lon + lon_delta
                        )
                        
                        for prop in nearby_properties:
                            distance = haversine_distance(lat, lon, prop.lat, prop.lon)
                            if distance <= radius_miles:
                                self.object.properties.add(prop)
                        
                        return response
            
            # If no changes to address/radius, just save normally
            return super().form_valid(form)


class DeleteListView(CustomLoginRequiredMixin, DeleteView):
    """Define a view to delete a list."""
    
    model = List
    template_name = 'project/delete_list_form.html'
    context_object_name = 'list'
    
    def get_queryset(self):
        """Restrict deletes to lists owned by the logged-in user."""
        return List.objects.filter(creator__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""
        
        # Calling the superclass method
        context = super().get_context_data(**kwargs)
        
        # Get profile from logged in user
        profile = self.get_profile()
        
        # Add viewer_profile for navbar
        context['viewer_profile'] = profile
        return context
    
    def get_success_url(self):
        """Redirect to the profile page after deleting a list."""
        return reverse('show_profile')


class ExportListView(CustomLoginRequiredMixin, View):
    """Define a view to export a list to CSV."""
    
    def get(self, request, *args, **kwargs):
        """Handle the GET request and return a CSV file."""
        # Get the list object
        list_pk = self.kwargs.get('pk')
        marketing_list = List.objects.get(pk=list_pk)
        
        # Verify the user owns this list
        profile = self.get_profile()
        if marketing_list.creator != profile:
            return redirect('show_profile')
        
        # Create the HttpResponse object with CSV header
        # Django documentation for CSV output
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{marketing_list.list_name}_properties.csv"'
        
        # Create CSV writer
        writer = csv.writer(response)
        
        # Write header row
        writer.writerow([
            'Property Address',
            'City',
            'Zip Code',
            'Style',
            'Year Built',
            'Owner Name',
            'Owner Address',
            'Owner Type',
            'Assessed Value',
            'Latitude',
            'Longitude'
        ])
        
        # Write data rows
        for property in marketing_list.properties.all():
            writer.writerow([
                property.address,
                property.city,
                property.zip_code,
                property.style,
                property.year_built,
                property.owner.name,
                property.owner.address,
                'Company' if property.owner.is_company else 'Individual',
                property.assessed_value,
                property.lat,
                property.lon
            ])
        
        return response


class LogoutConfirmationView(TemplateView):
    """Define a view to show logout confirmation."""
    
    template_name = 'project/logged_out.html'


class CreateListMapView(CustomLoginRequiredMixin, View):
    """Define a view to show the map-based list creation interface."""
    
    template_name = 'project/create_list_map.html'
    
    def get(self, request):
        """Display the map interface with limited property data."""
        profile = UserProfile.objects.get(user=request.user)
        
        # Don't load all properties - let the frontend request them as needed
        # Just pass an empty array, properties will be loaded via AJAX when user clicks
        properties_data = []
        
        import json
        context = {
            'viewer_profile': profile,
            'properties_json': json.dumps(properties_data),
            'form': CreateListMapForm()
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Handle the map-based list creation."""
        profile = UserProfile.objects.get(user=request.user)
        
        form = CreateListMapForm(request.POST)
        
        if form.is_valid():
            # Create the list
            new_list = form.save(commit=False)
            new_list.creator = profile
            new_list.center_address = "" # Blank address signals map-based list
            new_list.save()
            
            # Get data from form
            center_lat = new_list.center_lat
            center_lon = new_list.center_lon
            radius_miles = new_list.radius_miles
            
            # Find properties within radius
            # Using the same bounding box logic as in CreateListView
            lat_delta = radius_miles / 69.0
            lon_delta = radius_miles / 50.0
            
            nearby_properties = Property.objects.filter(
                lat__gte=center_lat - lat_delta,
                lat__lte=center_lat + lat_delta,
                lon__gte=center_lon - lon_delta,
                lon__lte=center_lon + lon_delta
            )
            
            # Calculate exact distances and add properties within radius
            for prop in nearby_properties:
                distance = haversine_distance(center_lat, center_lon, prop.lat, prop.lon)
                if distance <= radius_miles:
                    new_list.properties.add(prop)
            
            # Redirect to the list detail page
            return redirect('show_list', pk=new_list.pk)
        
        # If form is invalid, re-render with errors
        properties_data = []
        import json
        context = {
            'viewer_profile': profile,
            'properties_json': json.dumps(properties_data),
            'form': form
        }
        return render(request, self.template_name, context)
