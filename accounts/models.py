from django.db import models
from django.contrib.auth.models import User


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    cnpj = models.CharField('CNPJ', max_length=20, unique=True)
    company_name = models.CharField('Razão Social / Nome da Empresa', max_length=200)
    phone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    address = models.CharField('Endereço', max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.company_name} ({self.cnpj})"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    cpf = models.CharField('CPF', max_length=14, unique=True)
    phone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    address = models.CharField('Endereço', max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.cpf}"