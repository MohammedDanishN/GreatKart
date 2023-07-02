from .models import Category


def menu_links(request):
    category = Category.objects.all()
    return dict(links=category)
