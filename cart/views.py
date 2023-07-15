from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from .models import Cart, CartItem
from store.models import Product, Variation
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # fetch product
    product_variation = []
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

        # try and except for checking if the type and value exists in the db or not
            try:
                variation = Variation.objects.get(product=product,
                                                  variation_type__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except Exception as E:
                print(E)

    # trying to fetch cart_id , if not found create new cart
    try:
        # fetch card_id for the present session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    is_cart_item_exist = CartItem.objects.filter(
        product=product, cart=cart).exists()

    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        ex_var_list = []
        id = []
        for item in cart_item:
            ex_variation = item.variation.all()
            ex_var_list.append(list(ex_variation))
            id.append(item.id)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                for item in product_variation:
                    cart_item.variation.add(item)

            cart_item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product, quantity=1, cart=cart)
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)
        cart_item.save()
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Exception as E:
        pass
    return redirect('cart')


def delete_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(
        cart=cart, product=product, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def checkout(request, total_amount=0, quantity=0, cart_items=None, tax=0, grand_total=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total_amount += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (12*total_amount)/100
        grand_total = tax+total_amount
    except Exception as E:
        print(E)
    context = {'total_amount': float(total_amount), 'tax': tax, 'grand_total': grand_total,
               'quantity': quantity, 'cart_items': cart_items}
    return render(request, 'cart/checkout.html', context)


def cart(request, total_amount=0, quantity=0, cart_items=None, tax=0, grand_total=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total_amount += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (12*total_amount)/100
        grand_total = tax+total_amount
    except Exception as E:
        print(E)
    context = {'total_amount': float(total_amount), 'tax': tax, 'grand_total': grand_total,
               'quantity': quantity, 'cart_items': cart_items}

    return render(request, 'cart/cart.html', context)
