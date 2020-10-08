from django.db import models
from django.contrib.auth.models import AbstractUser
from djstripe.models import Subscription, Customer
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    customer = models.ForeignKey(
        Customer, null=True, blank=True, on_delete=models.SET_NULL,
        help_text="The user's Stripe Customer object, if it exists"
    )
    subscription = models.ForeignKey(
        Subscription, null=True, blank=True, on_delete=models.SET_NULL,
        help_text="The user's Stripe Subscription object, if it exists"
    )

    def __str__(self):
        return (self.email)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super(CustomUser,self).save(*args,**kwargs)
