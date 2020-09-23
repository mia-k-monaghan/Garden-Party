from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.HomeView.as_view(), name='index'),
    path('<pk>/detail/', views.ItemDetailView.as_view(),name='detail'),
    path('create-payment-intent',views.createpayment,name='create-payment-intent'),
    path('payment-complete',views.paymentcomplete,name='payment-complete'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('shipping/', views.ShippingView.as_view(), name='shipping')

]
