from django.contrib import admin
from .models import (
    Product, 
    Category, 
    Brand, 
    ProductPhoto
)


class ProductPhotoInline(admin.TabularInline): 
    model = ProductPhoto
    extra = 0


@admin.register(Product) 
class ProductAdmin(admin.ModelAdmin): 
    list_display = ['barcode', 'brand', 'title', 'volume', 'weight',
                    'price'] 
    search_fields = ['brand__title', 'title', 'barcode', 'description']
    inlines = [
        ProductPhotoInline,
    ]


@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ['title'] 
    search_fields = ['title']


@admin.register(Brand) 
class BrandAdmin(admin.ModelAdmin): 
    list_display = ['title'] 
    search_fields = ['title']