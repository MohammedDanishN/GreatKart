from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import razorpay

from store.models import Product
from .models import Order, Payment, OrderProduct
from cart.models import Cart, CartItem
from cart.views import _cart_id
from .forms import OrderForm

# Create your views here.


def payment_success(request):
    try:
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        razorpay_order_id = request.GET.get('razorpay_order_id')
        razorpay_signature = request.GET.get('razorpay_signature')
        print("*****************************")
        print(razorpay_payment_id + razorpay_order_id + razorpay_signature)
        order = Order.objects.get(
            user=request.user, is_ordered=False, order_number=razorpay_order_id)
        print("order done")
        # storing payment details in payment models
        payment = Payment.objects.create(user=request.user, razorpay_order_id=razorpay_order_id,
                                         payment_id=razorpay_payment_id, payment_method='UPI', amount_paid=order.order_total, status='PAID')
        print("Payment done")
        order.payment = payment
        order.is_ordered = True
        order.save()

        cart = Cart.objects.get(cart_id=_cart_id(request))
        print("cart done")
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        print(cart_items)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            print("got cart_item")
            product_variation = cart_item.variation.all()
            print("got variation")
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            print("got orderproduct")
            orderproduct.variations.set(product_variation)
            orderproduct.save()

            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        return HttpResponse("payment successfull")
    except Exception as E:
        print(E)
        return HttpResponse("Error Occured during payment")


def payment(request):
    client = razorpay.Client(
        auth=("rzp_test_yI4UspJjzX8pTz", "fiRvusdM5wlbKXQDY6zO5Qa6"))
    paymant = client.order.create(
        {'amount': 1000, 'currency': 'INR', 'payment_capture': 1})
    print(paymant)

    return HttpResponse("done")
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
            # yr = int(datetime.date.today().strftime('%Y'))
            # dt = int(datetime.date.today().strftime('%d'))
            # mt = int(datetime.date.today().strftime('%m'))
            # d = datetime.date(yr, mt, dt)
            # current_date = d.strftime("%Y%m%d")  # 20210305
            # order_number = current_date + str(data.id)
            client = razorpay.Client(
                auth=("rzp_test_JS9oedZq6XE4mW", "0YPgECxjeZzRo3JL9hofXqUh"))
            payment_detail = {"amount": grand_total*100, "currency": "INR"}
            payment = client.order.create(data=payment_detail)
            order_number = payment['id']
            data.order_number = order_number
            print(payment)
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total_amount': total_amount,
                'tax': tax,
                'grand_total': grand_total,
                'payment': payment
            }
            return render(request, 'orders/payment.html', context)
    else:
        return redirect('checkout')
