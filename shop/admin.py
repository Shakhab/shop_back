from django.contrib import admin
from shop.models import Product


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'sku', 'price', 'status')
