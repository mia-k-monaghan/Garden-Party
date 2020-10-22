from django.db import models
from django.contrib.auth.models import AbstractUser
from djstripe.models import Subscription, Customer
from django.utils.functional import cached_property
from djstripe.utils import subscriber_has_active_subscription
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(models.Model):
    user = models.CharField(max_length=50)
#     email = models.EmailField(_('email address'), unique=True)
#     customer = models.ForeignKey(
#         Customer, null=True, blank=True, on_delete=models.SET_NULL,
#         help_text="The user's Stripe Customer object, if it exists"
#     )
#     subscription = models.ForeignKey(
#         Subscription, null=True, blank=True, on_delete=models.SET_NULL,
#         help_text="The user's Stripe Subscription object, if it exists"
#     )

#     @cached_property
#     def has_active_subscription(self):
#         """Checks if a user has an active subscription."""
#         return subscriber_has_active_subscription(self)

#     def __str__(self):
#         return (self.email)

#     def save(self, *args, **kwargs):
#         if not self.username:
#             self.username = self.email
#         super(CustomUser,self).save(*args,**kwargs)

class LaunchSignUp(models.Model):
    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return (self.email)
