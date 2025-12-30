from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, time, timedelta

from .models import Category, Trip, TripEvent, Booking


# Write your tests here

"""
Test Category Creation & Slug Generation
"""
class CategoryModelTest(TestCase):
    # Confirms database save and verifies automatic slug generation

    def test_category_is_saved_with_slug(self):
        category = Category.objects.create(name="Hiking Trips")
        self.assertEqual(category.slug, "hiking-trips")
        self.assertEqual(Category.objects.count(), 1)


"""
Test Trip Creation & Helper Methods
"""

class TripModelTest(TestCase):
# Tests DB save and helper methods (price_display, star_rating)
    def setUp(self):
        self.category = Category.objects.create(name="Cycling")

        self.image = SimpleUploadedFile(
            name='test.jpg',
            content=b'',
            content_type='image/jpeg'
        )

    def test_trip_is_saved_and_helpers_work(self):
        trip = Trip.objects.create(
            category=self.category,
            title="Mountain Ride",
            place_name="Lake District",
            distance=25.5,
            duration="3 hours",
            level="Intermediate",
            main_image=self.image,
            price=50.00,
            sustainability_score=4
        )

        self.assertEqual(Trip.objects.count(), 1)
        self.assertEqual(trip.slug, "mountain-ride")
        self.assertEqual(trip.price_display(), "£50.00")
        self.assertEqual(trip.star_rating(), "★★★★☆")


"""
Test TripEvent Creation & Available Places
"""
class TripEventModelTest(TestCase):

    def setUp(self):
        category = Category.objects.create(name="Kayaking")
        image = SimpleUploadedFile("test.jpg", b"", content_type="image/jpeg")

        self.trip = Trip.objects.create(
            category=category,
            title="River Kayak",
            place_name="Wales",
            distance=10,
            duration="2 hours",
            level="Beginner",
            main_image=image,
            price=30.00
        )

    def test_event_available_places(self):
        event = TripEvent.objects.create(
            trip=self.trip,
            date=timezone.now().date() + timedelta(days=1),
            time=time(10, 0),
            max_places=10,
            booked_places=3
        )

        self.assertEqual(event.available_places, 7)
        self.assertEqual(event.status, "upcoming")


"""
Test Booking Creation & Database Update
"""
class BookingModelTest(TestCase):

    # Tests booking save and automatic update of booked_places

    def setUp(self):
        category = Category.objects.create(name="Walking")
        image = SimpleUploadedFile("test.jpg", b"", content_type="image/jpeg")

        trip = Trip.objects.create(
            category=category,
            title="Forest Walk",
            place_name="Surrey",
            distance=5,
            duration="1 hour",
            level="Beginner",
            main_image=image,
            price=20.00
        )

        self.event = TripEvent.objects.create(
            trip=trip,
            date=timezone.now().date() + timedelta(days=1),
            time=time(9, 0),
            max_places=10
        )

    def test_booking_is_saved_and_places_updated(self):
        booking = Booking.objects.create(
            trip=self.event,
            name="John Doe",
            email="john@example.com",
            num_people=2,
            price=20.00
        )

        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(self.event.booked_places, 2)
        self.assertEqual(booking.total_amount, 40.00)


"""
Test Prevent Overbooking
"""


def test_booking_cannot_exceed_available_places(self):
    with self.assertRaises(ValidationError):
        Booking.objects.create(
            trip=self.event,
            name="Jane Doe",
            email="jane@example.com",
            num_people=50,
            price=20.00
        )


"""
Test Prevent Booking Past Event
"""
class PastEventBookingTest(TestCase):

    def test_cannot_book_past_event(self):
        category = Category.objects.create(name="Climbing")
        image = SimpleUploadedFile("test.jpg", b"", content_type="image/jpeg")

        trip = Trip.objects.create(
            category=category,
            title="Rock Climb",
            place_name="Snowdonia",
            distance=8,
            duration="4 hours",
            level="Advanced",
            main_image=image,
            price=60.00
        )

        past_event = TripEvent.objects.create(
            trip=trip,
            date=timezone.now().date() - timedelta(days=1),
            time=time(10, 0)
        )

        with self.assertRaises(ValidationError):
            Booking.objects.create(
                trip=past_event,
                name="Alex",
                email="alex@example.com",
                num_people=1,
                price=60.00
            )
