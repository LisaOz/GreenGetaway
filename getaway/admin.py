from django.contrib import admin
from .models import Category, Trip

# Register models

"""
Here we register the models to display them on the admin site
"""

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'place_name', 'category', 'distance_display', 'duration', 'level', 'price_display')
    list_filter = ('category', 'level')
    search_fields = ('title', 'place_name')
    prepopulated_fields = {"slug": ("title",)}