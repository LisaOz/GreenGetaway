from django.urls import path
from . import views


app_name = "getaway"

urlpatterns = [
    path('', views.homepage, name='homepage'),           # homepage showing categories/trips
    path('trip/<slug:slug>/', views.trip_detail, name='trip_detail'),  # single trip page
]