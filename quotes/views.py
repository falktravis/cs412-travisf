# File: views.py
# Author: Travis Falk(travisf@bu.edu), 9/9/2025
# Description: View definitions for quotes app

from django.shortcuts import render
from django.http import HttpResponse, HttpResponse

import random

# Global Variables

# **Array of Wayne Gretsky Quotes
quote_array = [
    "You miss 100% of the shots you don't take.",
    "I just want to be the best.",
    "It's not about the destination, it's about the journey."
]

# Array of Wayne Gretsky Image URLs
image_array = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Andrew_Scheer_with_Wayne_Gretzky_%2848055697168%29_%28cropped%29.jpg/500px-Andrew_Scheer_with_Wayne_Gretzky_%2848055697168%29_%28cropped%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Wayne_Gretzky_statue_at_Star_Plaza%2C_downtown_LA%2C_USA_-_panoramio.jpg/500px-Wayne_Gretzky_statue_at_Star_Plaza%2C_downtown_LA%2C_USA_-_panoramio.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Wgretz_edit2.jpg/500px-Wgretz_edit2.jpg"
]

# Create your views here.
def quote(request):
    """View function for home page of site."""

    # Quote Page Template Route
    return_template = "quotes/quote.html"

    # Context containing the rendered quote and image
    context = {
        'quote': quote_array[random.randint(0, len(quote_array) - 1)],
        'image': image_array[random.randint(0, len(image_array) - 1)]
    }

    return render(request, return_template, context)

def show_all(request):
    """View function for showing all quotes."""

    # Show All Page Template Route
    return_template = "quotes/show_all.html"

    # Context containing all quotes and images
    context = {
        'quotes': quote_array,
        'images': image_array
    }

    return render(request, return_template, context)

def about(request):
    """View function for about page of site."""

    # About Page Template Route
    return_template = "quotes/about.html"

    return render(request, return_template)