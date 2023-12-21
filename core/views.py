from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView


from .models import Item, Order, OrderItem, Category



# Create your views here.
class HomeView(ListView):
    model = Item
    template_name = "core/home-page.html"
    context_object_name = "products"
    paginate_by = 4


class ProductView(DetailView):
    model = Item
    template_name = "core/product-page.html"
    context_object_name = "product"
    
product_view = ProductView.as_view()
    

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, request):
        try:
            orders_qs = Order.objects.filter(user = request.user, ordered = False)
           
            orders = orders_qs.first()
            items = orders.items.all()
            context = {
                "orders":orders, 
                "items":items
            }
            return render(request, "core/order_summary.html", context)
        except:
            messages.info(request, "You do not have any active order!")
            return redirect("/")

    
order_summary = OrderSummaryView.as_view()

# add item in the order summary page
def increase_item_qty(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    ordered_item, created = OrderItem.objects.get_or_create(item = item, user = request.user, ordered = False )

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            ordered_item.quantity += 1
            ordered_item.save()
            messages.info(request, "cart updated!")
        else:
            order.items.add(ordered_item)
            # order_item.quantity += 1
        return redirect("order-summary")
    else:
        messages.info(request, "You dont have an active order!")
        return redirect('/')

# reduces the item in the order summary page
def decrease_item_qty(request, slug):
    item = get_object_or_404(Item, slug=slug)
    ordered_item = OrderItem.objects.get(item=item, user=request.user, ordered = False)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug):
            if ordered_item.quantity > 1:
                ordered_item.quantity -= 1
                ordered_item.save()
                messages.info(request, "cart updated!")
            else:
                order.items.remove(ordered_item)
                messages.info(request, f"{ordered_item.item.title} order removed!")
        else:
            messages.info(request, f"no order for {item}")
    else:
        messages.info(request, "You have no active order!")

    return redirect("order-summary")

# Removes an ordered item in the order summary page
def remove_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get(item = item, user = request.user, ordered = False)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug):
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            messages.info(request, f"{order_item.item} order removed!")
        else:
            messages.info(request, f'you have no order for {item}!')
    else:
        messages.info(request, "You have no active order!")
    return redirect("order-summary")

class CheckoutView(View):
    def get(self, request):

        return render(request, "core/checkout-page.html")
    
    def post(self, request):
        print("pass")

checkout_view = CheckoutView.as_view()

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    ordered_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered = False)
    print("or it  ", type(ordered_item))
    order_qs = Order.objects.filter(user=request.user, ordered = False)

    # check if order exists
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            ordered_item.quantity += 1
            ordered_item.save()
            messages.info(request, "Item increased by one")
        else:
            order.items.add(ordered_item)
            messages.info(request, f"{ordered_item} added")
    else:
        current_time = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=current_time)
        order.items.add(ordered_item)
        messages.info(request, "cart updated")
    return redirect("product", slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered = False)

    if order_qs.exists():
        order = order_qs.first()
        print(order.items)
        if order.items.filter(item__slug=slug).exists():
            order_item = OrderItem.objects.filter(user=request.user, ordered = False, item=item).first()
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.success(request, "cart item reduced by one")
            else:
                order_item.save()
                order.items.remove(order_item)
                messages.info(request, "items removed!")
        else:
            messages.info(request, "No specified item in your ordered item")
            return redirect("product", slug=slug)

            
    else:
        messages.info(request, "You do not have any active order")
        return redirect("product", slug=slug)

    
    print('---> ', order_item)
    return redirect("product", slug=slug)





