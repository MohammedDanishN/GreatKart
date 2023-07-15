from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime

from .models import Order
from cart.models import Cart, CartItem
from cart.views import _cart_id
from .forms import OrderForm

# Create your views here.


def payment(request):
    return render(request, 'orders/payment.html')


def place_order(request):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    if cart_items.count() <= 0:
        return redirect('store')

    total_amount = 0
    tax = 0
    quantity = 0
    for cart_item in cart_items:
        total_amount += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (12*total_amount)/100
    grand_total = tax+total_amount

    if request.method == "POST":
        current_user = request.user
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total_amount': total_amount,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payment.html', context)
    else:
        return redirect('checkout')
