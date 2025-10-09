from django.urls import path
from . import views


app_name = "getaway"

urlpatterns = [
    path('', views.home, name='home'),           # homepage showing categories/trips
    path('category/<slug:slug>/', views.category_trips, name='category_trips'), #  for category

    path('trip/<slug:slug>/', views.trip_detail, name='trip_detail'),  #  for trip detail page

]