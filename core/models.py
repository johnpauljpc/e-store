from django.db import models
from django.shortcuts import reverse 
from django.contrib.auth import get_user_model

# Create your models here.
USER = get_user_model()

LABEL_CHOICES = (
    ('New', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class Category(models.Model):
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(null = True, blank = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    label = models.CharField(choices = LABEL_CHOICES, max_length=10)
    description = models.TextField()
    slug = models.SlugField()


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product", kwargs={"slug":self.slug})
    
    def add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"slug":self.slug})
    
    # remove from cart
    def remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"slug":self.slug})
    
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    user = models.ForeignKey(USER, on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)

    def get_total_item_discount_price(self):
        num_items = self.quantity
        price = self.item.discount_price
        total = num_items * price
        return total
    
    def amount_saved(self):
        dic_price = self.item.discount_price
        price = self.item.price
        saved_cost = (price - dic_price) * self.quantity
        return saved_cost

    def get_total_item_price(self):
        num_items = self.quantity
        price = self.item.price
        total = num_items * price
        return total
    
    def get_final_total_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        else:
            return self.get_total_item_price()

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class Order(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add= True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def order_total(self):
        total = 0
        for ordered_item in self.items.all():
            total += ordered_item.get_final_total_price()
        return total

    def __str__(self):
        return f'{self.user.first_name} | order'