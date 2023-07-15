from django.contrib import admin

# Register your models here.
from .models import Order, Payment, OrderProduct


admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)
