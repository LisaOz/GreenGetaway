from django.urls import path
from .views import CategoryList, TripList, TripDetail, trip_list

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('trips/', TripList.as_view()),
    path('trips/', trip_list, name='trip_list'),
    path('trips/<int:pk>/', TripDetail.as_view()),
]