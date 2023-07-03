from django.shortcuts import render, redirect

from .models import Cart, CartItem
from store.models import Product
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # fetch product

    # trying to fetch cart_id , if not found create new cart
    try:
        # fetch card_id for the present session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    # fetching item, if already present then quantity++ ,else create new item
    try:
        cart_item = CartItem.objects.get(product=product)
        cart_item.quantity += 1
        cart_item.save()
    except:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
        )
    cart_item.save()
    print(cart_item.product)
    return redirect('cart')


def cart(request):
    return render(request, 'cart/cart.html')
