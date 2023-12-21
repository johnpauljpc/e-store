from django import template
import inflect

from core.models import Order

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered = False )
        if qs.exists():
            order = qs.first()
            ordered_items = order.items.all()
            total = sum([item.quantity for item in ordered_items])
            # items = order.items.quantity
            return total

        return 0

    else:
        return 0




# to interpret numbers to words
p = inflect.engine()

@register.filter
def number_to_words(value):
    return p.number_to_words(value, andword='and', zero='zero').replace(',', '').replace("point zero", "")
