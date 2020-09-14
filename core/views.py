# import random
# import string
#
from django.conf import settings
from django.utils.decorators import method_decorator
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from djstripe.models import Product, Plan
from .models import Cart
from django.views.decorators.csrf import csrf_exempt
# from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, View, CreateView
import stripe
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from .forms import SubscribeForm

# stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
# def create_ref_code():
#     return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
#

class HomeView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

class CartView(ListView, LoginRequiredMixin):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        filter_val = self.request.user
        new_context = Cart.objects.filter(user=filter_val)
        return new_context




class ItemDetailView(DetailView):
    model = Product
    template_name = 'item_detail.html'

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product:
        cart = Cart.objects.get_or_create(
            user = request.user,
            item = product
        )
        cart[0].save()

    # add_cart = Profile.objects.get_or_create(
    #     user = request.user,
    #     cart = set(product)
    # )
    # add_cart.save()
    return redirect('core:index')

@login_required
def checkout(request):
    if request.user.is_authenticated:
        form=SubscribeForm()
        products = Product.objects.all()
        product = Product.objects.filter(name='Classic Garden Party')[0]
        total = Plan.objects.filter(product=product)[0].amount
        return render(request, 'checkout.html', {'products':products, 'product':product, 'total':total, 'form':form})
    else:
        redirect('core:index')

@csrf_exempt
def createpayment(request):
    if request.user.is_authenticated:
        #TODO: get request product to work
        product = Product.objects.filter(name='Classic Garden Party')[0]
        total = Plan.objects.filter(product=product)[0].amount

        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        if request.method=="POST":

            data = json.loads(request.body)
            intent = stripe.PaymentIntent.create(
                amount=int(total*100),
                currency=data['currency'],
                metadata={'integration_check': 'accept_a_payment'},

                )
            try:
                return JsonResponse({'publishableKey':
                    settings.STRIPE_TEST_PUBLIC_KEY, 'clientSecret': intent.client_secret})
            except Exception as e:
                return JsonResponse({'error':str(e)},status= 403)
@csrf_exempt
def paymentcomplete(request):
    if request.method=='POST':
        data = json.loads(request.POST.get('payload'))
        if data['status'] == 'succeeded':
            pass
        return render(request, 'payment-complete.html')

#
class SubscribeView(View):

    def get(self, *args,**kwargs):
        form = SubscribeForm()
        context= {
            'form':form
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = SubscribeForm(self.request.POST)
        # pk = self.kwargs['pk']
        # item = Product.objects.filter(pk=pk)[0]

        if form.is_valid():
            shipping_address = Address.objects.get_or_create(
                user=self.request.user,
                street_address = form.cleaned_data.get('shipping_street_address'),
                apartment_address = form.cleaned_data.get('shipping_apartment_address'),
                state = form.cleaned_data.get('shipping_state'),
                zip = form.cleaned_data.get('shipping_zip'),
                address_type = 'S'

            )
            shipping_address[0].save()

            # billing_address = Address.objects.get_or_create(
            #     user=self.request.user,
            #     street_address = form.cleaned_data.get('billing_street_address'),
            #     apartment_address = form.cleaned_data.get('billing_apartment_address'),
            #     state = form.cleaned_data.get('billing_state'),
            #     zip = form.cleaned_data.get('billing_zip'),
            #     address_type = 'B'
            #
            # )
            # billing_address[0].save()

            # OrderSetting.objects.create(
            #     user=self.request.user,
            #     item=item,
            #     shipping_address=shipping_address[0],
            #     billing_address=billing_address[0]
            # )
        return HttpResponseRedirect(reverse('core:index'))
