

from django.shortcuts import render, get_object_or_404
from .models import Category, Trip

# Create your views here.


"""
View for a homepage
"""


def domestic_trips(request):
    categories = Category.objects.all()
    return render(request, 'getaway/domestic_trips.html', {'categories': categories})

"""
View for a separate trip with description and other details
"""
def trip_detail(request, slug):
    trip = get_object_or_404(Trip, slug=slug)
    return render(request, 'getaway/trip_detail.html', {'trip': trip})