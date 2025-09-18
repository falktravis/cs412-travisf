# File: views.py
# Author: Travis Falk(travisf@bu.edu), 9/17/2025
# Description: View definitions for restaurant app

from django.shortcuts import render
from django.http import HttpResponse, HttpResponse

import random
import time

# Global Variables

specials = [
    "Ragù",
    "Grilled Salmon with Asparagus",
    "Lamb Chops with Rosemary",
    "Lobster Fra Diavolo",
]

# Create your views here.
def main(request):
    """View function for home page of site."""

    # Main Page Template Route
    return_template = "restaurant/main.html"

    return render(request, return_template)

def order(request):
    """View function for order page."""

    # Order Page Template Route
    return_template = "restaurant/order.html"

    context = {
        "special": specials[random.randint(0, len(specials) - 1)]
    }

    return render(request, return_template, context)

def confirmation(request):
    """View function for confirmation page of site."""

    # Confirmation Page Template Route
    return_template = "restaurant/confirmation.html"

    # Context definition for scope
    context = {
        # Set time to 30-60 minutes from now
        "readytime": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() + random.randint(1800, 3600)))
    }

    print(request.POST)

    # Get form data if POST request
    if request.POST:

        # Initialize empty order list
        order = []
        # Initialize price
        price = 0.0

        if request.POST.get('spaghetti'):
            item = "Spaghetti"
            price += 15.0
            if request.POST.get('meatballs'):
                item += "  with Meatballs"
                price += 3.0
            if request.POST.get('sausage'):
                item += "  with Sausage"
                price += 3.0
            order.append(item)
        if request.POST.get('lasagna'):
            order.append("Lasagna")
            price += 12.0
        if request.POST.get('fettuccine'):
            order.append("Fettuccine Alfredo")
            price += 14.0
        if request.POST.get('special'):
            order.append("Special")
            price += 18.0

        # Get form data
        context = {
            # Set time to 30-60 minutes from now
            "readytime": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() + random.randint(1800, 3600))),
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "instructions": request.POST.get("instructions"),
            "order": order,
            "price": price,
        }

        print(context)

    return render(request, return_template, context)