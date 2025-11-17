from rest_framework import serializers
from getaway.models import Category, Trip, Booking
from rest_framework import serializers
from getaway.models import Trip
from getaway.models import Booking, TripEvent

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'trip', 'name', 'email', 'num_people', 'created_at', 'price', 'paid']
        read_only_fields = ['id', 'created_at', 'paid']

