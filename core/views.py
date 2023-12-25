from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.http import HttpResponse
import uuid



from .models import Item, Order, OrderItem, Category, BillingAddress, Payment
from .forms import CheckoutForm
from .utils import flutterwave, paystack




# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = "core/home-page.html"
    context_object_name = "products"
    paginate_by = 4
    ordering = ('-id')


class ProductView(DetailView):
    model = Item
    template_name = "core/product-page.html"
    context_object_name = "product"
    
product_view = ProductView.as_view()
    

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, request):
        try:
            orders = Order.objects.get(user = request.user, ordered = False)
            items = orders.items.all()
            context = {
                "orders":orders, 
                "items":items
            }
            
        except:
            messages.info(request, "You do not have any active order!")
            return redirect("/")
        return render(request, "core/order_summary.html", context)
    
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


class CheckoutView(LoginRequiredMixin,View):
    def get(self, request):
        print(request.user)
        print(request.user.id)
        form = CheckoutForm()
        order = None

        try:
            order = Order.objects.get(user = request.user, ordered = False)
            if not(order.items.all().exists()):
                raise Exception
        except:
            messages.info(request, "You have no order!")
            return redirect("/")   
        context = {
            "form":form,
            "order":order
        }

        return render(request, "core/checkout-page.html", context)
    
    def post(self, request):
        form = CheckoutForm(request.POST)
        order = None
        
        
        try:
            order = Order.objects.get(user = request.user, ordered = False)
            if order is None:
                raise ObjectDoesNotExist
            
            print("order")
            context = {
            "form":form,
            "order":order
            }
            
            if form.is_valid():
                shipping_zip = form.cleaned_data.get('shipping_zip')
                state = form.cleaned_data.get("state")
                shipping_address = form.cleaned_data.get("shipping_address")
                phone_number  = form.cleaned_data.get("phone_number")
                payment_option = form.cleaned_data.get("payment_option")
                print("form    ", form.cleaned_data)
                address = BillingAddress.objects.create(user = request.user, state=state,  shipping_zip=shipping_zip,
                                         shipping_address = shipping_address, 
                                        phone_number = phone_number)
                print("address    ", address)
                address.save()
                print("order   --")
                order.billing_address = address
                order.save()
                messages.info(request, "address details saved!")

                # Redirects to payment view
                return redirect("payment", payment_option = payment_option)
            else:
                messages.info(request, "checkout failed!")
                return redirect("checkout")
        except ObjectDoesNotExist:
            print(order)
            messages.warning(request, "You do not have an active order")
            return redirect("/")
        

checkout_view = CheckoutView.as_view()



class PaymentView(View):
    def get(self, request, payment_option):
        ref = str(timezone.now().date())+request.user.first_name+str(uuid.uuid4())

        try:
            order = Order.objects.get(user = request.user, ordered = False)
            if order is None:
                raise Exception
        except:
            messages.warning(request, "You don't have any active order!")
            return redirect("/")
        payment = Payment.objects.create(
            order = order,
            customer = request.user,
            ref = ref,
            amount = order.order_total(),
            payment_option = payment_option
        )
        payment.save()
        order.payment = payment
        order.save()
    
        if payment_option == "flutterwave":
            try:
                return redirect (flutterwave.process_payment(order, ref))
            except Exception as error:
                messages.error(request, f"error in flutterwave payment  {error}")
        
        elif payment_option == "paystack":
            try:
                return redirect(paystack.process_payment(order, ref))
            except Exception as err:
                messages.error(request, f"error --->  {err}")
                return redirect("/")
        else:
            print("its invalid ")
        
        return HttpResponse(f"{payment_option} is invalid")
    

payment_view = PaymentView.as_view()


# Confirm payment
def confirm_payment(request, ref):
    status = request.GET.get('status')
    am = request.GET.get('amount')
    payment_opt = None
    try:
        payment = Payment.objects.get(ref = ref)
        order = Order.objects.get(payment__ref = payment.ref)
        payment_opt = order.payment.payment_option

    except:
        messages.error(request, "something is wrrong!")
        return redirect("/")
    
    # validate transaction of fluterwave
    if payment_opt == "flutterwave":
        if status != "successful":
            return redirect('cancel-payment')
    payment.completed = True
    order.ordered = True
    order.total = order.order_total()

    payment.save()
    order.save()

    messages.success(request, "your payment is successful and confirmed")
    return redirect('/')
    return HttpResponse(f"{payment} |  {order.order_total()}")

def cancel_payment(request):
    messages.warning(request, "payment cancelled (' _ ') !")
    return redirect("checkout")