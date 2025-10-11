from django.urls import path
from . import views


app_name = "getaway"

urlpatterns = [

    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_trips, name='category_trips'),
    path('trip/<slug:slug>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:trip_id>/book/', views.book_trip, name='book_trip'),

]

