from django.urls import path
from . views import *

urlpatterns = [
    path('place_order/', place_order, name='place_order'),
    path('payment/', payment, name='payment'),
    path('success/', payment_success, name='success'),

]
