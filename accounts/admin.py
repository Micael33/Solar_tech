from django.contrib import admin
from .models import SellerProfile, CustomerProfile


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name','cnpj','user')
    search_fields = ('company_name','cnpj','user__username')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user','cpf')
    search_fields = ('user__username','cpf')
