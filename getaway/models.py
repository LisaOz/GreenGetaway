from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
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
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

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
        return self.max_places - self.booked_places

    def save(self, *args, **kwargs):
        now = timezone.now()
        event_datetime = timezone.make_aware(datetime.combine(self.date, self.time))

        if self.status != 'cancelled':
            self.status = 'passed' if event_datetime < now else 'upcoming'
        super().save(*args, **kwargs)


# ---------- BOOKING MODEL ----------
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(TripEvent, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    places = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.event.status in ['passed', 'cancelled']:
            raise ValueError(f"Cannot book this trip. Current status is '{self.event.status}'.")

        if self.places > self.event.available_places:
            raise ValueError(f"Only {self.event.available_places} places are available for this trip.")

        super().save(*args, **kwargs)
        self.event.booked_places += self.places
        self.event.save()

    def __str__(self):
        return f"{self.user.username} booked {self.places} place(s) for {self.event}"
