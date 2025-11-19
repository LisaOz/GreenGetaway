from django.urls import path
from .views import CategoryList, TripList, TripDetail, register
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('trips/', TripList.as_view()),
    path('trips/<int:pk>/', TripDetail.as_view()),

    # Booking endpoint
    path('bookings/', views.booking_create, name='booking-create'),

    # Authentication
    path("register/", register, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]