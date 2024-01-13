from django.contrib import admin
from .models import Order, OrderItem, Category, Item, BillingAddress,Payment, Coupon

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered_date', 'ordered', 'total', 'billing_address', "display_items"]

    list_filter = ['user', 'ordered_date', 'ordered', 'total']
    list_display_links = ['user', 'billing_address']

class PaymentAmin(admin.ModelAdmin):
    list_display = ['customer', 'amount', 'payment_option', "completed"]
    list_filter = ['customer',  'payment_option', "completed"]



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(BillingAddress)
admin.site.register(Payment, PaymentAmin)
admin.site.register(Coupon)