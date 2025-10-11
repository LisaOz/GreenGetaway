from decimal import Decimal
from django.conf import settings
from .models import TripEvent


"""
Class Cart. The customer will add their trips to the cart to either save, book or remove them
"""
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, trip_event, quantity=1):
        trip_id = str(trip_event.id)
        if trip_id not in self.cart:
            self.cart[trip_id] = {'quantity': 0, 'title': trip_event.title}
        self.cart[trip_id]['quantity'] += quantity
        self.save()

    def remove(self, trip_event):
        trip_id = str(trip_event.id)
        if trip_id in self.cart:
            del self.cart[trip_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        trip_ids = self.cart.keys()
        trips = TripEvent.objects.filter(id__in=trip_ids)
        for trip in trips:
            yield {
                'trip': trip,
                'quantity': self.cart[str(trip.id)]['quantity'],
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
