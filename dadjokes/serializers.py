# File: serializers.py
# Author: Travis Falk (travisf@bu.edu), 11/13/2025
# Description: Serializer definitions for dadjokes app REST API

from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    '''Serializer for the Joke model.'''
    
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'timestamp']
    
    def create(self, validated_data):
        '''Override the create method to handle joke creation.'''
        joke = Joke.objects.create(**validated_data)
        return joke


class PictureSerializer(serializers.ModelSerializer):
    '''Serializer for the Picture model.'''
    
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'timestamp']
