from django.shortcuts import render
# from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm
from django.views.generic import ListView, DetailView, View, FormView, UpdateView, CreateView
from django.contrib.auth import views as auth_views

from .models import CustomUser

# Create your views here.
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

class ProfileView(DetailView):
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'user'


class ProfileUpdate(UpdateView):
    model = CustomUser
    template_name = 'user_update.html'
    context_object_name = 'user'

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
