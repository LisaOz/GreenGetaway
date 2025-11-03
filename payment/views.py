from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from getaway.models import Booking
from .models import Payment
import stripe

# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_create(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'unit_amount': int(booking.price * 100),  # Stripe uses pence
                'product_data': {
                    'name': f'Booking #{booking.id}',
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
    return render(request, "payment/completed.html")


def payment_cancel(request):
    return render(request, "payment/cancel.html")