from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from getaway.models import Category, Trip
from .serializers import CategorySerializer, TripSerializer, BookingSerializer

# Create your views here.
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