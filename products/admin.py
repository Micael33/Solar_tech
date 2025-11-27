from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','seller','price','quantity')
    search_fields = ('name','seller__company_name')
    list_filter = ('seller',)