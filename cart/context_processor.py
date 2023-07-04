from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    cart_count = 0
    try:
        cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))

        for item in cart_items:
            cart_count += item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    return {'cart_count': cart_count}
