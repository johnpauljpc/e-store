from django.contrib import admin
from .models import Order, OrderItem, Category, Item, BillingAddress,Payment, Coupon

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)