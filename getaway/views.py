from django.shortcuts import render, get_object_or_404
from .models import Category, Trip


# Create your views here.


"""
View for a homepage
"""


def home(request):
    categories = [
        {'name': 'City Strolls', 'image': 'getaway/images/city.jpg'},
        {'name': 'Nature Retreats', 'image': 'getaway/images/nature.jpg'},
        {'name': 'Abroad Travels', 'image': 'getaway/images/abroad.jpg'},
    ]
    return render(request, 'getaway/home.html', {'categories': categories})



"""
View for a category
"""

def category_trips(request, slug):
    category = get_object_or_404(Category, slug=slug)
    trips = category.trips.all()  # using related_name='trips'
    return render(request, 'getaway/category_trips.html', {
        'category': category,
        'trips': trips
    })



"""
View for a separate trip with description and other details
"""

def trip_detail(request, slug):
    trip = get_object_or_404(Trip, slug=slug)
    events = trip.events.filter(status='upcoming')
    return render(request, 'getaway/trip_detail.html', {'trip': trip, 'events': events})



