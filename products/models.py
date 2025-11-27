from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Product(models.Model):
    seller = models.ForeignKey('accounts.SellerProfile', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Link externo para imagem (ex: https://exemplo.com/imagem.png)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']


    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - R$ {self.price}"