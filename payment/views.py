import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import Booking


stripe.api_key = settings.STRIPE_SECRET_KEY

# ----------------------------
# Payment creation
# ----------------------------
def payment_create(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Save booking ID in session to access after payment success
    request.session['booking_id'] = booking.id

    # Total amount for Stripe (in pence)
    trip_price = booking.trip.trip.price or 0
    total_amount = trip_price * booking.num_people
    stripe_amount = int(total_amount * 100)  # GBP to pence

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
        metadata={'booking_id': str(booking.id)},  # important for webhook
    )

    return redirect(checkout_session.url)


# ----------------------------
# Payment completed
# ----------------------------
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


# ----------------------------
# Send confirmation email
# ----------------------------
def send_confirmation_email(booking):
    subject = f"Booking Confirmation - ID {booking.id}"
    message = render_to_string('emails/booking_confirmation.txt', {
        'booking': booking,
        'total_amount': booking.trip.trip.price * booking.num_people,
    })

    email = EmailMessage(
        subject,
        message,
        'GreenGetaway@example.com',  # From
        [booking.email],             # To
    )
    email.content_subtype = "plain"
    email.send()


# ----------------------------
# Payment cancelled
# ----------------------------
def payment_cancel(request):
    return render(request, "payment/cancel.html")


# ----------------------------
# Stripe webhook
# ----------------------------

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event=None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)  # Invalid payload
    except Exception:
        return HttpResponse(status=400)  # Invalid signature

    # Handle successful payment
    if event.type == 'checkout.session.completed':
        session = event.data.object

        # Retrieve booking ID from metadata
        booking_id = session.metadata.get('booking_id') if hasattr(session, 'metadata') else None
        if booking_id:
            try:
                booking = Booking.objects.get(id=booking_id)
                booking.paid = True
                booking.save()

                # Update booked places
                booking.trip.booked_places += booking.num_people
                booking.trip.save()
            except Booking.DoesNotExist:
                pass

    return HttpResponse(status=200)
