from django.db import models
from django.utils.text import slugify

# Create your models here.

"""
These are models for Category - City Strolls and Nature retreats and the Trip
"""

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"  # Plural form for admin
    def __str__(self):
        return self.name

class Trip(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True) # slug
    place_name = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=6, decimal_places=2, help_text="Distance in km")
    duration= models.CharField(max_length=50, help_text="Duration of trip")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    main_image = models.ImageField(upload_to='trip_images/')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"

    def __str__(self):
        return f"{self.title} ({self.place_name})"



        # Auto-generate slug when saving

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)