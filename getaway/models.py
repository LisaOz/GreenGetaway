from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime

# ---------- CATEGORY MODEL ----------
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ---------- TRIP MODEL ----------
class Trip(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    place_name = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=6, decimal_places=2, help_text="Distance in km")
    duration = models.CharField(max_length=50, help_text="Duration of trip")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    main_image = models.ImageField(upload_to='trip_images/')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # Price per person

    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"

    def price_display(self):
        if self.price is not None:
            return f"£{self.price:.2f}"
        return "Free"
    price_display.short_description = "Price"

    def distance_display(self):
        return f"{self.distance} km"
    distance_display.short_description = "Distance"

    def __str__(self):
        return f"{self.title} ({self.place_name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# ---------- TRIP IMAGE MODEL ----------
class TripImage(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='trip_images/')


# ---------- TRIP EVENT MODEL ----------
class TripEvent(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('passed', 'Passed'),
        ('cancelled', 'Cancelled'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='events')
    date = models.DateField()
    time = models.TimeField()
    max_places = models.PositiveIntegerField(default=20)
    booked_places = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.trip.title} on {self.date} at {self.time}"

    @property
    def available_places(self):

        # Return remaining available places for the trip event
        return self.max_places - self.booked_places

    @property
    def price_per_person(self):
        # Return the price per person from the related Trip.
        return self.trip.price or 0

    def save(self, *args, **kwargs):
        # Automatically update status based on current datetime.
        now = timezone.now()
        event_datetime = datetime.combine(self.date, self.time)

        # Ensure timezone awareness
        if timezone.is_naive(event_datetime):
            event_datetime = timezone.make_aware(event_datetime)

        if self.status != 'cancelled':
            self.status = 'passed' if event_datetime < now else 'upcoming'
        super().save(*args, **kwargs)


# ---------- BOOKING MODEL ----------
class Booking(models.Model):
    trip = models.ForeignKey(TripEvent, on_delete=models.CASCADE, related_name='bookings')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    num_people = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def clean(self):
        # Validate that the number of people does not exceed available places.
        if self.num_people > self.trip.available_places:
            from django.core.exceptions import ValidationError
            raise ValidationError(f"Not enough available places for this trip event. Only {self.trip.available_places} left.")

    def save(self, *args, **kwargs):
        # Call clean() before saving to enforce validation.
        self.clean()
        super().save(*args, **kwargs)
        # Update booked_places on the TripEvent
        self.trip.booked_places += self.num_people
        self.trip.save()

    @property
    def total_amount(self):
        # Calculate total price for the booking.
        return self.num_people * self.trip.price

    def __str__(self):
        return f"Booking by {self.name} for {self.trip}"
