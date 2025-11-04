from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from getaway.models import Booking
from .models import Payment
import stripe
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY

"""
Vies for payment in the process with all details
"""


def payment_create(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Save booking ID in session to access it after payment success
    request.session['booking_id'] = booking.id

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


"""
View for successfully completed payment with the confirmation email with all detaild
"""


def payment_completed(request):
    booking_id = request.session.get('booking_id')
    booking = None

    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)

        # Send confirmation email
        send_confirmation_email(booking)

        # Clear booking_id from session
        del request.session['booking_id']

    return render(request, "payment/completed.html", {'booking': booking})


"""
View for confirmation email after successful payment
"""


def send_confirmation_email(booking):
    subject = f"Booking Confirmation - ID {booking.id}"
    message = render_to_string('emails/booking_confirmation.txt', {
        'booking': booking,
        'total_amount': booking.total_amount,
    })

    email = EmailMessage(
        subject,
        message,
        'GreenGetaway@example.com',  # From
        [booking.email],             # To
    )
    email.content_subtype = "plain"
    email.send() # Send confirmation email in the text file


"""
View for cancelled booking
"""


def payment_cancel(request):
    return render(request, "payment/cancel.html")
