from django.contrib import admin
from .models import Pharmacy, Medicine, Inventory, Order, OrderItem, Delivery

admin.site.register(Pharmacy)
admin.site.register(Medicine)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)
