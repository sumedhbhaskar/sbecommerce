from django.contrib import admin
from django.urls import path, include
from .views import HomeView, CheckoutView, ItemView, OrderSummaryView, add_to_cart, remove_from_cart,decrease_single_item_from_cart 

app_name = 'core'

urlpatterns = [ 
    
    path('', HomeView.as_view(), name="home-page"),
    path('checkout/', CheckoutView.as_view(), name='checkout-page'),
    path('product/<slug>/', ItemView.as_view(), name = 'product-page'),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name = 'remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('decrease-single-item-from-cart/<slug>/',decrease_single_item_from_cart, name = 'decrease-single-item-from-cart')
]
