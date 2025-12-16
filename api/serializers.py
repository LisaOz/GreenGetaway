from getaway.models import Category, Trip, Booking
from rest_framework import serializers
from getaway.models import Trip
from getaway.models import Booking, TripEvent



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    stars_and_score = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            'id', 'category', 'title', 'slug', 'place_name', 'distance',
            'duration', 'level', 'main_image', 'description', 'price',
            'sustainability_score', 'stars_and_score'
        ]

    def get_stars_and_score(self, obj):
        # Hard-coded 5 stars
        return "★★★★★ (5/5)" # hardcoded version
            # dynamic version:
            # stars = "★" * obj.sustainability_score + "☆" * (5 - obj.sustainability_score)
            # return f"{stars} ({obj.sustainability_score}/5)"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'trip', 'name', 'email', 'num_people', 'created_at', 'price', 'paid']
        read_only_fields = ['id', 'created_at', 'paid']

