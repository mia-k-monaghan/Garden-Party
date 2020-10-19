from django.db import models
from djstripe.models import Product
from django.conf import settings
from django.shortcuts import reverse
from localflavor.us.models import USStateField,USZipCodeField
# Create your models here.


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='address')
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    state = USStateField()
    zip = USZipCodeField()
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.address_type}) {self.street_address}"

    class Meta:
        verbose_name_plural = 'Addresses'

class MonthlyOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE, unique_for_month='date')
    date = models.DateField(auto_now_add=True)
    prepared = models.BooleanField(default=False)
    tracking = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user}"
