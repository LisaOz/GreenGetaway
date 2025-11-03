from django.contrib import admin
from .models import Payment

# Register your models here.


"""
To display payments in Django admin
"""


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
