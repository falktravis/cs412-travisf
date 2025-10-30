# File: urls.py
# Author: Travis Falk(travisf@bu.edu), 10/29/2025
# Description: URL patterns for voter_analytics app

from django.urls import path
from . import views

urlpatterns = [
    # map the URL (empty string) to the view
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path('graphs/', views.GraphsView.as_view(), name='graphs'),
]
