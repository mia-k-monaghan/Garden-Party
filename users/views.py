from django.shortcuts import render
# from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm
from django.views.generic import ListView, DetailView, View, FormView, UpdateView, CreateView
from django.contrib.auth import views as auth_views
from djstripe.models import PaymentMethod

from .models import CustomUser, LaunchSignUp
from core.models import Address

# Create your views here.
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

class ProfileView(View):

    def get(self, *args, **kwargs):
        user = self.request.user
        address = Address.objects.filter(user=user)[0]
        last4 = self.request.user.customer.default_payment_method.card['last4']


        context = {
            'user':user,
            'last4': last4,
            'address_pk': address.pk,
            'street_address':address.street_address,
            'apt_address':address.apartment_address,
            'city':address.city,
            'state':address.state,
            'zip':address.zip,
        }
        return render(self.request, 'users/user_detail.html', context)



class ProfileUpdate(UpdateView):
    model = CustomUser
    template_name = 'users/user_update.html'
    fields = ['first_name', 'last_name', 'email',]

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('users:account',args=[pk])

class SignupView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def get_success_url(self):
        return reverse_lazy('core:shipping')

    def form_valid(self, form):
        valid = super(SignupView, self).form_valid(form)
        username, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        user = authenticate(username=username,
                            password=password)
        login(self.request, user)
        return valid

class LaunchView(CreateView):
    model = LaunchSignUp
    template_name = 'launch.html'
    fields = ['email']

    def get_success_url(self):
        return reverse_lazy('users:launch-success')

def LaunchSuccessView(request):
    return render(request, 'users/launch_success.html')
