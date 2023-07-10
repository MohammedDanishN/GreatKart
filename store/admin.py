from django.contrib import admin
from .models import Product, Variation
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'price',
                    'stock', 'is_available', 'category']
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Product, ProductAdmin)


class VariationAmdin(admin.ModelAdmin):
    list_display = ['product', 'variation_type',
                    'variation_value', 'is_active']
    list_editable = ['is_active']


admin.site.register(Variation, VariationAmdin)
