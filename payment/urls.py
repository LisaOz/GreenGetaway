from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path("create/<int:booking_id>/", views.payment_create, name="create"),
    path("completed/", views.payment_completed, name="completed"),
    path("cancel/<int:booking_id>/", views.payment_cancel, name="cancel"),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'), # ulr for webhook (for Stripe payments notifications)
]