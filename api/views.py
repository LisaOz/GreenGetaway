from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from django.conf import settings
from getaway.models import Category, Trip, Booking
from .serializers import CategorySerializer, TripSerializer, BookingSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe
import json

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhook endpoint to handle events like checkout.session.completed.
    This endpoint is CSRF-exempt because Stripe cannot send a CSRF token.
    """

    # 1️. Read the raw request body and Stripe signature header
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    # 2️. Verify the webhook signature
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # 3️. Handle the Stripe event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # 4️. Extract metadata and customer details
        trip_id = session['metadata'].get('trip_id')
        num_people = session['metadata'].get('num_people')
        name = session['metadata'].get('name')
        email = session.get('customer_email')  # email sent by Stripe

        # 5. Convert numeric fields
        try:
            trip_id = int(trip_id)
            num_people = int(num_people)
        except (TypeError, ValueError):
            # If conversion fails, skip creating booking
            return HttpResponse(status=400)

        # 6️. Create the Booking in your database
        try:
            Booking.objects.create(
                trip_id=trip_id,
                name=name,
                email=email,
                num_people=num_people,
                paid=True  # mark as paid since payment succeeded
            )
            print(f"Booking created: trip {trip_id}, {num_people} person(s), email: {email}")
        except Exception as e:
            print(f"Error creating booking: {e}")
            return HttpResponse(status=500)

    # 7️. Return 200 to acknowledge receipt of the webhook
    return HttpResponse(status=200)

"""
Endpoint for Payment intent creation with the CSRF exemption, so this endpoint will ignore CSRF
and could be used in mobile app
"""
@csrf_exempt # Exempt CSRF because Flutter POST won’t send CSRF token
def create_payment_intent(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)
    amount = data.get("amount")

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="gbp",
        )
        return JsonResponse({"clientSecret": intent.client_secret})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

"""
Endpoint for checkout session
"""


@csrf_exempt  # Important! Flutter POST won’t send CSRF
def create_checkout_session(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)


    try:
        data = json.loads(request.body)
        print("PARSED JSON:", data)

        amount = data.get("amount")
        trip_id = data.get("trip_id")
        name = data.get("name")
        email = data.get("email")
        num_people = data.get("num_people")

        if not all([amount, trip_id, name, email, num_people]):
            print("Missing required fields!")
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # Deep link redirect
        success_url = f"greengetaway://booking-success?trip_id={trip_id}&num_people={num_people}"
        cancel_url = "greengetaway://payment-cancelled"

        # Create Stripe session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "gbp",
                    "product_data": {"name": f"Trip Booking ID {trip_id}: {name}"},
                    "unit_amount": amount,
                },
                "quantity": 1,
            }],
            mode="payment",

            cancel_url=f"{settings.FRONTEND_URL}/booking-cancel/",
            customer_email=email,
            metadata={
                "trip_id": str(trip_id),
                "num_people": str(num_people),
                "name": name,
                "email": email
            }
        )


        print("Stripe session created:", session.id)
        return JsonResponse({"checkout_url": session.url})

    except Exception as e:
        print("STRIPE ERROR:", str(e))
        return JsonResponse({"error": str(e)}, status=400)

"""
CategoryList APIView to give Flutter list of trip categories.
"""

class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


""" 
TripList gives all trips, filtered by category slug. 
"""
class TripList(APIView):
    def get(self, request):
        trips = Trip.objects.all()

        category = request.GET.get('category')
        if category:
            trips = trips.filter(category__slug=category)

        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)


"""
TripDetail APIView gives the detail of a single trip (for "Trip detail" page)
"""

class TripDetail(APIView):
    def get(self, request, pk):
        trip = Trip.objects.get(id=pk)
        serializer = TripSerializer(trip)
        return Response(serializer.data)



@api_view(['POST'])
def booking_create(request):
    """
    API endpoint to create a new booking from Flutter app.
    Expects JSON with: trip, name, email, num_people, and price
    """
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # saves booking in DB
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({"message": "User registered successfully"}, status=201)
