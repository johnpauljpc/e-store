from django.urls import path

from .views import (HomeView, product_view, add_to_cart, remove_from_cart,
                     order_summary, increase_item_qty, decrease_item_qty, remove_item,
                     checkout_view)

urlpatterns=[
    path("", HomeView.as_view(), name="home"),
    path("product/<slug>/",product_view, name="product" ),

    path("order-summary/", order_summary, name="order-summary"),
    path("increase-item/<slug:slug>/", increase_item_qty, name="increase-item-qty"),
    path("decrease-item/<slug:slug>/", decrease_item_qty, name="decrease-item-qty"),
    path("remove-order-item/<slug:slug>/", remove_item, name="remove-item"),

    path("add-to-cart/<slug:slug>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug:slug>/", remove_from_cart, name="remove-from-cart"),

    path("checkout/", checkout_view, name="checkout"),





]