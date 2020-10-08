from django.conf import settings
from django.utils.decorators import method_decorator
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from djstripe.models import Product, Plan
from .models import Cart, Address as A
from users.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
# from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, View, CreateView
import stripe
import json
import djstripe
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from .forms import SubscribeForm

class HomeView(ListView):
    model = Product
    template_name = 'core/index.html'
    context_object_name = 'products'


class ItemDetailView(DetailView):
    model = Product
    template_name = 'core/item_detail.html'


@csrf_exempt
@login_required
def createpayment(request):
    custom_user = request.user
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    if request.method=="POST":
        data = json.loads(request.body)
        payment_method = data['payment_method']
        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

        try:
            # This creates a new Customer and attaches the PaymentMethod in one API call.
	        customer = stripe.Customer.create(
	            payment_method=payment_method,
	            email=request.user.email,
	            invoice_settings={
	                'default_payment_method': payment_method
	            }
	        )
	        djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
	        custom_user.customer = djstripe_customer


	        # Subscribe the user to the subscription created
	        subscription = stripe.Subscription.create(
	            customer=customer.id,
	            items=[
	                {
	                    "price": data["price_id"],
	                },
	            ],
	            expand=["latest_invoice.payment_intent"]
	        )
	        djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)
	        custom_user.subscription = djstripe_subscription
	        custom_user.save()
	        return JsonResponse(subscription)
        except Exception as e:
            return JsonResponse({'error':str(e)},status= 403)
def paymentcomplete(request):
    return render(request, 'core/payment-complete.html')

#
class CheckoutView(LoginRequiredMixin,View):
    def get(self, *args,**kwargs):
        products = Product.objects.all()
        product = Product.objects.filter(name='Classic Garden Party')[0]
        total = Plan.objects.filter(product=product)[0].amount

        context= {
            'products':products,
            'product':product,
            'total':total
        }
        return render(self.request, 'core/checkout.html', context)


class ShippingView(LoginRequiredMixin, View):

    def get(self, *args,**kwargs):
        form = SubscribeForm()

        context= {
            'form':form,
        }
        return render(self.request, 'core/shipping.html', context)

    def post(self, *args, **kwargs):
        form = SubscribeForm(self.request.POST)

        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = self.request.user
            new_address.address_type = "S"
            new_address.save()

        return HttpResponseRedirect(reverse('core:checkout'))

    
