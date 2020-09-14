from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.HomeView.as_view(), name='index'),
    path('<pk>/detail/', views.ItemDetailView.as_view(),name='detail'),
    path('create-payment-intent',views.createpayment,name='create-payment-intent'),
    path('payment-complete',views.paymentcomplete,name='payment-complete'),
    path('<pk>/add-to-cart', views.add_to_cart, name='add'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.CartView.as_view(), name='cart'),
    # path('subscribe/',views.SubscribeView.as_view(),name='subscribe'),
    # path('')

]
