from django.contrib import admin
from django.urls import path, include
from . import views  # views for the getaway app


app_name = 'getaway'

urlpatterns = [
  #  path('admin/', admin.site.urls), # moved it to the project level

    # Getaway app URLs
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_trips, name='category_trips'),
    path('trip/<slug:slug>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:trip_id>/book/', views.book_trip, name='book_trip'),

    ]