from django.contrib import admin
from .models import Order, OrderItem, Category, Item, BillingAddress

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(BillingAddress)