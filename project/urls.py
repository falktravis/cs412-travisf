# File: urls.py
# Author: Travis Falk(travisf@bu.edu), 12/2/2025
# Description: URL patterns for project app

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # Main pages
    path('', ShowProfileView.as_view(), name='show_profile'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    
    # Profile pages
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    
    # Property pages
    path('properties/', PropertyListView.as_view(), name='show_all_properties'),
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='show_property'),
    
    # List pages
    path('list/<int:pk>/', ListDetailView.as_view(), name='show_list'),
    path('list/create/', CreateListView.as_view(), name='create_list'),
    path('list/create/map/', CreateListMapView.as_view(), name='create_list_map'),
    path('list/<int:pk>/update/', UpdateListView.as_view(), name='update_list'),
    path('list/<int:pk>/delete/', DeleteListView.as_view(), name='delete_list'),
    path('list/<int:pk>/export/', ExportListView.as_view(), name='export_list'),
]
