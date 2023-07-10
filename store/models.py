from django.db import models
from django.urls import reverse

from category.models import Category


# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/product')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_type='color', is_active='True')

    def sizes(self):
        return super(VariationManager, self).filter(variation_type='size', is_active='True')


variation_type_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_type = models.CharField(
        max_length=50, choices=variation_type_choice)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
