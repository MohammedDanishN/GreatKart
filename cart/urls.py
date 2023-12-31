from django.urls import path

from .views import *


urlpatterns = [
    path('', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>',
         remove_cart_item, name='remove_cart'),
    path('delete_cart/<int:product_id>/<int:cart_item_id>',
         delete_cart_item, name='delete_cart'),
    path('checkout', checkout, name="checkout")
]
