from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Trip, TripEvent, TripImage
from .forms import TripEventForm
from .models import Booking


# ---------- Inline for extra images ----------
class TripImageInline(admin.TabularInline):
    model = TripImage
    extra = 5  # number of blank slots to show


# ---------- Trip Admin with inline ----------
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    inlines = [TripImageInline]
    list_display = (
        'title', 'place_name', 'category',
        'distance_display', 'duration', 'level', 'price_display'
    )
    list_filter = ('category', 'level')
    search_fields = ('title', 'place_name')
    prepopulated_fields = {"slug": ("title",)}


# ---------- Category Admin ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


# ---------- TripEvent Admin ----------
@admin.register(TripEvent)
class TripEventAdmin(admin.ModelAdmin):
    form = TripEventForm
    list_display = ('trip', 'date', 'time', 'status', 'available_places_display')
    list_filter = ('status', 'date', 'trip')
    search_fields = ('trip__title',)

    # Custom display for available places with color warnings
    def available_places_display(self, obj):
        remaining = obj.available_places
        if remaining == 0:
            return format_html('<span style="color:red;font-weight:bold;">Sold Out</span>')
        elif remaining <= 5:
            return format_html('<span style="color:orange;">{} left</span>', remaining)
        else:
            return f"{remaining} available"

    available_places_display.short_description = 'Available Places'


# ---------- Booking Admin ----------

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'trip', 'num_people', 'created_at')
    list_filter = ('trip__trip__title', 'created_at')  # filter by trip title and date
    search_fields = ('name', 'email', 'trip__trip__title')