from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings
from getaway.models import Category, Trip
from .serializers import CategorySerializer, TripSerializer, BookingSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe
import json



# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
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
# Set your Stripe secret key from Django settings
stripe.api_key = settings.STRIPE_SECRET_KEY

# Exempt this view from CSRF checks because Flutter app won't send CSRF token
@csrf_exempt
def create_checkout_session(request):
    # Ensure only POST requests are allowed
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        # Parse JSON data from request body
        data = json.loads(request.body)

        # Extract relevant fields from request
        amount = data.get("amount")  # total amount in pence
        currency = data.get("currency", "gbp")  # default to GBP
        trip_id = data.get("trip_id")  # trip being booked
        name = data.get("name")  # customer name
        email = data.get("email")  # customer email
        num_people = data.get("num_people")  # number of people booking

        # Validate that all required fields are present
        if not all([amount, trip_id, name, email, num_people]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # Create a Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],  # Only allow card payments
            line_items=[{
                "price_data": {
                    "currency": currency,
                    "product_data": {
                        # Display name for the booking in Stripe Checkout
                        "name": f"Trip Booking ID {trip_id}: {name}",
                    },
                    "unit_amount": amount,  # Stripe expects amount in the smallest currency unit (pence)
                },
                "quantity": 1,  # Only 1 line item for the booking
            }],
            mode="payment",  # Single payment
            # Where the user is redirected after successful payment
            success_url=f"{settings.FRONTEND_URL}/booking-success/?trip_id={trip_id}&num_people={num_people}",
            # Where the user is redirected if they cancel the payment
            cancel_url=f"{settings.FRONTEND_URL}/booking-cancel/",
            customer_email=email,  # Prefill email in Stripe Checkout
        )

        # Return the URL of the Stripe Checkout session to the Flutter app
        return JsonResponse({"checkout_url": session.url})

    except Exception as e:
        # Return any errors as JSON to the Flutter app
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
