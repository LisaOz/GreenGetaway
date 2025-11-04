from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from getaway.models import Booking
from .models import Payment
import stripe

# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_create(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Get the price from the Trip related to this Booking
    trip_price = booking.trip.trip.price or 0
    total_amount = trip_price * booking.num_people
    stripe_amount = int(total_amount * 100)  # Convert pounds to pence for Stripe

    # Create the Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'unit_amount': stripe_amount,
                'product_data': {
                    'name': f"{booking.trip.trip.title} - {booking.trip.date} ({booking.num_people} people)",
                    'description': f"Booking ID: {booking.id}",
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/payment/completed/'),
        cancel_url=request.build_absolute_uri('/payment/cancel/'),
    )

    return redirect(checkout_session.url)



def payment_completed(request):
    return render(request, "payment/completed.html", {
        'redirect_url': 'getaway:home'  # or 'getaway:home'
    })


def payment_cancel(request):
    return render(request, "payment/cancel.html")