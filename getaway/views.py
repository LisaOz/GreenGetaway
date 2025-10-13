from .models import Category, Trip
from django.shortcuts import render, redirect, get_object_or_404
from .models import TripEvent
from .forms import BookingForm
from django.db.models import Min


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
View for the list of trips by category. The trips are displayed with newest upcoming on the top
"""


def category_trips(request, slug):
    category = get_object_or_404(Category, slug=slug)

    # Get trips in this category, ordered by the soonest event date
    trips = (
        category.trips
        .annotate(next_event_date=Min('events__date'))  # the earliest event date per trip
        .order_by('next_event_date')  # soonest trips first
    )

    return render(request, 'getaway/category_trips.html', {
        'category': category,
        'trips': trips
    })


"""
View for a separate trip with description and other details
"""

def trip_detail(request, slug):
    trip = get_object_or_404(Trip, slug=slug)
    first_event = trip.events.filter(status='upcoming').first()
    return render(request, 'getaway/trip_detail.html', {
        'trip': trip,
        'first_event': first_event
    })

"""
View for a booking form. Allows to book the first upcoming event
"""


def book_trip(request, trip_id):
    trip_event = get_object_or_404(TripEvent, id=trip_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.trip = trip_event

            # Check if enough slots are available
            if booking.num_people <= trip_event.available_places:
                booking.save()
                # Optionally update booked_places
                trip_event.booked_places += booking.num_people
                trip_event.save()
                return render(request, 'getaway/booking_success.html', {
                    'booking': booking,
                    'trip_event': trip_event
                })
            else:
                # Not enough places available
                return render(request, 'getaway/booking_failed.html', {
                    'trip_event': trip_event
                })
    else:
        form = BookingForm()

    return render(request, 'getaway/booking_form.html', {
        'form': form,
        'trip_event': trip_event
    })
