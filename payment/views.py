from django.shortcuts import render
import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from getaway.models import Booking
from .models import Payment

# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # If payment already exists, redirect to some page
    if hasattr(booking, 'payment'):
        return redirect('payment_success', payment_id=booking.payment.id)

    # Create Stripe payment intent
    intent = stripe.PaymentIntent.create(
        amount=int(booking.total_amount * 100),  # amount in pence
        currency='£',
        metadata={'booking_id': booking.id}
    )

    # Create Payment record with pending status
    payment = Payment.objects.create(
        booking=booking,
        amount=booking.total_amount,
        stripe_payment_intent=intent['id'],
        status='pending'
    )

    return render(request, 'payment/payment_page.html', {
        'booking': booking,
        'client_secret': intent.client_secret,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })