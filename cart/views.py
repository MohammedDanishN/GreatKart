from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
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


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def delete_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')


def cart(request, total_amount=0, quantity=0, cart_items=None, tax=0, grand_total=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total_amount += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (12*total_amount)/100
        grand_total = tax+total_amount
    except ObjectDoesNotExist:
        pass
    context = {'total_amount': float(total_amount), 'tax': tax, 'grand_total': grand_total,
               'quantity': quantity, 'cart_items': cart_items}
    return render(request, 'cart/cart.html', context)
