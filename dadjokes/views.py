# File: views.py
# Author: Travis Falk (travisf@bu.edu), 11/13/2025
# Description: View definitions for dadjokes app

from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render
from .models import Joke, Picture
import random

# REST API imports
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import JokeSerializer, PictureSerializer

# Create your views here.

class RandomView(TemplateView):
    '''View to display a random joke and random picture.'''
    template_name = 'dadjokes/random.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all jokes and pictures
        jokes = list(Joke.objects.all())
        pictures = list(Picture.objects.all())
        
        # Select random joke and picture if they exist
        if jokes:
            context['joke'] = random.choice(jokes)
        else:
            context['joke'] = None
            
        if pictures:
            context['picture'] = random.choice(pictures)
        else:
            context['picture'] = None
            
        return context


class ShowAllJokesView(ListView):
    '''View to display all jokes.'''
    model = Joke
    template_name = 'dadjokes/show_all_jokes.html'
    context_object_name = 'jokes'


class ShowJokeDetailView(DetailView):
    '''View to display a single joke.'''
    model = Joke
    template_name = 'dadjokes/show_joke.html'
    context_object_name = 'joke'


class ShowAllPicturesView(ListView):
    '''View to display all pictures.'''
    model = Picture
    template_name = 'dadjokes/show_all_pictures.html'
    context_object_name = 'pictures'


class ShowPictureDetailView(DetailView):
    '''View to display a single picture.'''
    model = Picture
    template_name = 'dadjokes/show_picture.html'
    context_object_name = 'picture'


# REST API Views

class JokeListAPIView(generics.ListCreateAPIView):
    '''API view to return a listing of Jokes and to create a Joke.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''API view to retrieve a single Joke by primary key.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class RandomJokeAPIView(APIView):
    '''API view to return a random Joke.'''
    
    def get(self, request):
        jokes = list(Joke.objects.all())
        if jokes:
            joke = random.choice(jokes)
            serializer = JokeSerializer(joke)
            return Response(serializer.data)
        return Response({})


class PictureListAPIView(generics.ListAPIView):
    '''API view to return a listing of Pictures.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    '''API view to retrieve a single Picture by primary key.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPictureAPIView(APIView):
    '''API view to return a random Picture.'''
    
    def get(self, request):
        pictures = list(Picture.objects.all())
        if pictures:
            picture = random.choice(pictures)
            serializer = PictureSerializer(picture)
            return Response(serializer.data)
        return Response({})
