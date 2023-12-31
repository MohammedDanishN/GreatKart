from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


from . models import Product
from category.models import Category
from cart.models import Cart, CartItem
from cart.views import _cart_id
# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True).order_by('id')
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        product_count = products.count()

    # pagination
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'product_count': product_count}
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()
    except Exception as e:
        raise e
    context = {'single_product': single_product, 'in_cart': in_cart}
    return render(request, 'store/product-detail.html', context)


def search(request):
    search_key = request.GET.get('search')
    if search_key:
        products = Product.objects.filter(
            Q(product_name__icontains=search_key) |
            Q(description=search_key))
    context = {
        'products': products,
        'product_count': products.count()
    }

    return render(request, 'store/store.html', context)
