from django.db import models
from djstripe.models import Product
from django.db.models.signals import post_save
from django.conf import settings
from django.shortcuts import reverse
from django.db.models import Sum
from django.dispatch import receiver
from localflavor.us.models import USStateField,USZipCodeField
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
#
#
# class Item(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     short_description = models.CharField(max_length = 50, null = True, blank=True)
#     description = models.TextField(blank=True, null=True)
#     slug = models.SlugField()
#     image = models.ImageField(upload_to='gallery')
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse("core:item", kwargs={
#             'slug': self.slug
#         })
#
#     def get_add_to_cart_url(self):
#         return reverse("core:add-to-cart", kwargs={
#             'slug': self.slug
#         })
#
#     def get_remove_from_cart_url(self):
#         return reverse("core:remove-from-cart", kwargs={
#             'slug': self.slug
#         })
#
# class OrderSetting(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     first_ordered = models.DateTimeField(null=True, blank=True)
#     last_ordered_date = models.DateTimeField(null=True, blank=True)
#     subscribed = models.BooleanField(default=True)
#     skip_next_shipment = models.BooleanField(default=False)
#     shipping_address = models.ForeignKey(
#         'Address', related_name='default_shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
#     billing_address = models.ForeignKey(
#         'Address', related_name='default_billing_address', on_delete=models.SET_NULL, blank=True, null=True)
#     payment = models.ForeignKey(
#         'Payment', related_name='default_payment', on_delete=models.SET_NULL, blank=True, null=True)
#
#
#     def __str__(self):
#         return f"{self.item.name}"
#
#     def get_final_price(self):
#         return self.item.price
#
# class Order(models.Model):
#     ref_code = models.CharField(max_length=20, blank=True, null=True)
#     item = models.ForeignKey(OrderSetting, on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     ordered_date = models.DateTimeField()
#     shipping_address = models.ForeignKey(
#         'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
#     billing_address = models.ForeignKey(
#         'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
#     payment = models.ForeignKey(
#         'Payment', on_delete=models.SET_NULL, blank=True, null=True)
#     tracking = models.CharField(max_length=50, blank=True, null=True)
#
#     def __str__(self):
#         return self.user.username
#
#     def get_total(self):
#         total = 0
#         for order_item in self.items.all():
#             total += order_item.get_final_price()
#         return total

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = USStateField()
    zip = USZipCodeField()
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.address_type}) {self.street_address}"

    class Meta:
        verbose_name_plural = 'Addresses'
#
# class Payment(models.Model):
#     stripe_charge_id = models.CharField(max_length=50)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.DecimalField(max_digits=6, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user.username
