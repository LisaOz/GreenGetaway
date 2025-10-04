

from django.shortcuts import render, get_object_or_404
from .models import Category, Trip

# Create your views here.


"""
View for a homepage
"""
def homepage(request):
    categories = Category.objects.all()
    trips = Trip.objects.all()
    return render(request, 'getaway/homepage.html', {'categories': categories, 'trips': trips})


"""
View for a separate trip with description and other details
"""
def trip_detail(request, slug):
    trip = get_object_or_404(Trip, slug=slug)
    return render(request, 'getaway/trip_detail.html', {'trip': trip})