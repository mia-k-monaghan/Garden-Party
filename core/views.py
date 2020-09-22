from django.conf import settings
from django.utils.decorators import method_decorator
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from djstripe.models import Product, Plan
from .models import Cart, Address as A
from django.views.decorators.csrf import csrf_exempt
# from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, View, CreateView
import stripe
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from .forms import SubscribeForm

class HomeView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'


class ItemDetailView(DetailView):
    model = Product
    template_name = 'item_detail.html'


@login_required
def checkout(request):
    form=SubscribeForm()
    products = Product.objects.all()
    product = Product.objects.filter(name='Classic Garden Party')[0]
    total = Plan.objects.filter(product=product)[0].amount

    if request.method=="POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            shipping_address = Address.objects.get_or_create(
                user=request.user,
                street_address = form.cleaned_data.get('shipping_street_address'),
                apartment_address = form.cleaned_data.get('shipping_apartment_address'),
                state = form.cleaned_data.get('shipping_state'),
                zip = form.cleaned_data.get('shipping_zip'),
                address_type = 'S'

            )
            shipping_address[0].save()

    return render(request, 'checkout.html', {'products':products, 'product':product, 'total':total, 'form':form})

@csrf_exempt
@login_required
def createpayment(request):
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
        return render(self.request, 'checkout.html', context)


class ShippingView(LoginRequiredMixin, View):

    def get(self, *args,**kwargs):
        form = SubscribeForm()

        context= {
            'form':form,
        }
        return render(self.request, 'shipping.html', context)

    def post(self, *args, **kwargs):
        form = SubscribeForm(self.request.POST)

        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = self.request.user
            new_address.address_type = "S"
            new_address.save()

        return HttpResponseRedirect(reverse('core:checkout'))


def createSub(request):
    if request.method == 'POST':
        street = request.POST.get('street')
        apt = request.POST.get('apt')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        response_data = {}

        address = A(
            user = request.user,
            street_address = street,
            apartment_address = apt,
            city = city,
            state = state,
            zip = zip,
            address_type = 'S'
        )
        address.save()

        response_data['result'] = 'Create post successful!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
