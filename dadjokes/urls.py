# File: urls.py
# Author: Travis Falk (travisf@bu.edu), 11/13/2025
# Description: URL patterns for dadjokes app

from django.urls import path
from .views import (
    RandomView, ShowAllJokesView, ShowJokeDetailView, 
    ShowAllPicturesView, ShowPictureDetailView,
    JokeListAPIView, JokeDetailAPIView, RandomJokeAPIView,
    PictureListAPIView, PictureDetailAPIView, RandomPictureAPIView
)

urlpatterns = [
    # Web views
    path('', RandomView.as_view(), name='random_joke_picture'),
    path('random', RandomView.as_view(), name='random'),
    path('jokes', ShowAllJokesView.as_view(), name='show_all_jokes'),
    path('joke/<int:pk>', ShowJokeDetailView.as_view(), name='show_joke'),
    path('pictures', ShowAllPicturesView.as_view(), name='show_all_pictures'),
    path('picture/<int:pk>', ShowPictureDetailView.as_view(), name='show_picture'),
    
    # API endpoints
    path('api/', RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/random', RandomJokeAPIView.as_view(), name='api_random'),
    path('api/jokes', JokeListAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name='api_joke_detail'),
    path('api/pictures', PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name='api_picture_detail'),
    path('api/random_picture', RandomPictureAPIView.as_view(), name='api_random_picture'),
]
