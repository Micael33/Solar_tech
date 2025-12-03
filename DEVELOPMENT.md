# 🛠️ Guia de Desenvolvimento - Solar Store

## 📝 Índice

1. [Setup de Desenvolvimento](#setup-de-desenvolvimento)
2. [Estrutura de Projeto](#estrutura-de-projeto)
3. [Padrões de Código](#padrões-de-código)
4. [Criando Novas Features](#criando-novas-features)
5. [Testes e Qualidade](#testes-e-qualidade)
6. [Git & Commits](#git--commits)
7. [Debugging](#debugging)
8. [Performance](#performance)

---

## 🚀 Setup de Desenvolvimento

### 1. Clonar e Configurar

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/solar-store.git
cd solar-store

# Criar virtual env
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Editar .env
# Copiar .env.example → .env
# Preencher STRIPE_KEYS etc

# Migrations
python manage.py migrate

# Criação de dados de teste
python manage.py shell
```

### 2. Estrutura de Diretórios para Desenvolvimento

```
solar-store/
├── .venv/                  # Virtual env (git-ignored)
├── venv/                   # Virtual env alt (git-ignored)
├── .git/                   # Git repo
├── .env                    # Variáveis (git-ignored)
├── .gitignore              # Git ignore patterns
├── manage.py               # Django CLI
├── requirements.txt        # Dependências
├── db.sqlite3              # Banco dev (git-ignored)
├── solar_store/            # Settings principal
├── accounts/               # App: Autenticação
├── products/               # App: Produtos
├── cart/                   # App: Carrinho
├── orders/                 # App: Pedidos
├── payments/               # App: Pagamentos
├── static/                 # CSS, JS, images
├── templates/              # HTML templates
├── tests/                  # Testes unitários
├── docs/                   # Documentação
└── scripts/                # Scripts utilitários
```

---

## 📚 Estrutura de Projeto

### Django Apps

Cada app Django segue este padrão:

```
app_name/
├── __init__.py
├── admin.py                # Registro no Django Admin
├── apps.py                 # Config da app
├── models.py               # Modelos de dados (ORM)
├── views.py                # Views e lógica
├── forms.py                # Formulários Django
├── urls.py                 # Roteamento interno
├── tests.py                # Testes unitários
├── migrations/             # Migrações de BD
│   ├── __init__.py
│   └── 0001_initial.py
└── templates/
    └── app_name/
        ├── list.html
        ├── detail.html
        └── form.html
```

### Nova App Django

```bash
# Criar app
python manage.py startapp minha_app

# Estrutura criada automaticamente:
minha_app/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── views.py
├── migrations/
│   └── __init__.py
```

### Registrar App

1. Criar `minha_app/apps.py`:
```python
from django.apps import AppConfig

class MinhaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'minha_app'
```

2. Adicionar em `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'minha_app',
]
```

3. Adicionar URLs em `solar_store/urls.py`:
```python
urlpatterns = [
    # ...
    path('minha_app/', include('minha_app.urls')),
]
```

---

## 🎯 Padrões de Código

### 1. Modelos (models.py)

```python
# ✅ Bom
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """Modelo de Produto no catálogo"""
    
    seller = models.ForeignKey(
        'accounts.SellerProfile',
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=255, help_text="Nome do produto")
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['seller', '-created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def is_available(self):
        """Verificar disponibilidade"""
        return self.quantity > 0
```

### 2. Views (views.py)

```python
# ✅ Bom
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@login_required
@require_http_methods(['GET', 'POST'])
def product_create(request):
    """
    View para criar novo produto (vendedor).
    
    GET: Retorna formulário vazio
    POST: Cria produto no banco
    """
    
    # Verificar autorização
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, 'Apenas vendedores podem criar produtos.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.save()
            
            messages.success(
                request,
                f'Produto "{product.name}" criado com sucesso!'
            )
            return redirect('product_detail', slug=product.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm()
    
    context = {'form': form}
    return render(request, 'products/product_form.html', context)


# ✅ Class-based view (alternativa)
from django.views import View
from django.views.generic import ListView, DetailView

class ProductListView(ListView):
    """View de listagem usando CBV"""
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.all()
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(
                name__icontains=query
            ) | queryset.filter(
                description__icontains=query
            )
        
        return queryset
```

### 3. Formulários (forms.py)

```python
from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class ProductForm(forms.ModelForm):
    """Formulário para criar/editar produtos"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do produto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição detalhada',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'R$ 0,00',
                'step': '0.01'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError('Preço deve ser maior que zero')
        return price
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity < 0:
            raise ValidationError('Quantidade não pode ser negativa')
        return quantity
```

### 4. URLs (urls.py)

```python
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Listagem
    path('', views.product_list, name='product_list'),
    
    # Criar
    path('novo/', views.product_create, name='product_create'),
    
    # Detalhe (sempre por último por causa do slug)
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Editar
    path('<slug:slug>/editar/', views.product_edit, name='product_edit'),
    
    # Deletar
    path('<slug:slug>/deletar/', views.product_delete, name='product_delete'),
]
```

### 5. Templates

```html
<!-- ✅ Bom: com context, i18n, herança -->
{% extends 'base/base.html' %}
{% load static %}
{% load i18n %}

{% block title %}{% trans "Criar Produto" %} - Solar Store{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/products.css' %}">
{% endblock %}

{% block content %}
<div class="container">
    <h1>{% trans "Novo Produto" %}</h1>
    
    {% if form.non_field_errors %}
        <div class="alert alert-danger">
            {{ form.non_field_errors }}
        </div>
    {% endif %}
    
    <form method="post" enctype="multipart/form-data" class="product-form">
        {% csrf_token %}
        
        {% for field in form %}
            <div class="form-group">
                <label for="{{ field.id_for_label }}">
                    {{ field.label }}
                </label>
                {{ field }}
                
                {% if field.errors %}
                    <div class="error-message">
                        {{ field.errors }}
                    </div>
                {% endif %}
            </div>
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">
            {% trans "Criar Produto" %}
        </button>
    </form>
</div>
{% endblock %}
```

---

## ✨ Criando Novas Features

### Checklist: Nova Feature

- [ ] Criar branch: `git checkout -b feature/descricao`
- [ ] Implementar modelo (models.py)
- [ ] Criar migração: `python manage.py makemigrations`
- [ ] Testar migração: `python manage.py migrate`
- [ ] Implementar views (views.py)
- [ ] Criar forms (forms.py)
- [ ] Escrever testes (tests.py)
- [ ] Criar templates (templates/)
- [ ] Adicionar CSS (static/css/)
- [ ] Atualizar URLs (urls.py)
- [ ] Documentar em README
- [ ] Fazer commit: `git commit -m "feat: descrição da feature"`
- [ ] Push: `git push origin feature/descricao`
- [ ] Criar Pull Request no GitHub

### Exemplo: Adicionar "Reviews" de Produtos

**1. Modelo (models.py):**
```python
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'customer')
```

**2. Migração:**
```bash
python manage.py makemigrations products
python manage.py migrate
```

**3. View:**
```python
@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.customer = request.user.customer_profile
            review.save()
            return redirect('product_detail', slug=slug)
    else:
        form = ReviewForm()
    
    return render(request, 'products/add_review.html', {'form': form})
```

**4. URL:**
```python
path('<slug:slug>/review/', views.add_review, name='add_review'),
```

**5. Template:**
```html
<!-- products/add_review.html -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Enviar Review</button>
</form>
```

---

## 🧪 Testes e Qualidade

### Estrutura de Testes

```
tests/
├── __init__.py
├── test_models.py           # Testes de modelos
├── test_views.py            # Testes de views
├── test_forms.py            # Testes de formulários
└── test_integration.py      # Testes de integração
```

### Exemplo: Teste de Modelo

```python
# tests/test_models.py
from django.test import TestCase
from products.models import Product
from accounts.models import SellerProfile
from django.contrib.auth.models import User

class ProductModelTest(TestCase):
    
    def setUp(self):
        """Preparar dados de teste"""
        self.user = User.objects.create_user(
            username='seller',
            password='123456'
        )
        self.seller = SellerProfile.objects.create(
            user=self.user,
            cnpj='12345678000100',
            company_name='Test Company'
        )
    
    def test_product_creation(self):
        """Testar criação de produto"""
        product = Product.objects.create(
            seller=self.seller,
            name='Test Product',
            slug='test-product',
            description='Test',
            price=100.00,
            quantity=10
        )
        
        self.assertEqual(product.name, 'Test Product')
        self.assertTrue(product.is_available())
    
    def test_product_unavailable(self):
        """Testar produto indisponível"""
        product = Product.objects.create(
            seller=self.seller,
            name='Test Product',
            slug='test-product-2',
            price=100.00,
            quantity=0
        )
        
        self.assertFalse(product.is_available())
```

### Exemplo: Teste de View

```python
# tests/test_views.py
from django.test import TestCase, Client
from django.contrib.auth.models import User

class ProductViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
    
    def test_product_list_view(self):
        """Testar listagem de produtos"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
    
    def test_product_create_view_requires_login(self):
        """Testar que create requer login"""
        response = self.client.get('/products/novo/')
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_product_create_view_authenticated(self):
        """Testar create com usuário logado"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/products/novo/')
        # Esperaria 403 se não for vendedor
        self.assertEqual(response.status_code, 302)
```

### Executar Testes

```bash
# Todos os testes
python manage.py test

# Teste específico
python manage.py test products.tests.ProductModelTest

# Com cobertura
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório em htmlcov/
```

---

## 📌 Git & Commits

### Boas Práticas

**Branch naming:**
```
feature/nome-feature           # Nova feature
bugfix/nome-bug                # Correção de bug
hotfix/nome-hotfix             # Hotfix urgente
docs/nome-doc                  # Documentação
refactor/nome-refactor         # Refatoração
```

**Commit messages (Conventional Commits):**
```
feat: adicionar reviews de produtos
fix: corrigir validação de preço
docs: atualizar documentação de API
style: formatar código CSS
refactor: refatorar ProductView
test: adicionar testes de Payment
chore: atualizar dependências
```

### Workflow Typical

```bash
# 1. Criar branch
git checkout -b feature/nova-funcionalidade

# 2. Fazer mudanças
# ... edit files ...

# 3. Adicionar mudanças
git add .
# ou específico:
git add products/views.py products/models.py

# 4. Commit
git commit -m "feat: adicionar suporte a Reviews"

# 5. Push
git push origin feature/nova-funcionalidade

# 6. Pull Request no GitHub
# ... criar PR, aguardar review ...

# 7. Após aprovação, merge
git checkout main
git pull origin main
git merge feature/nova-funcionalidade

# 8. Deletar branch
git branch -d feature/nova-funcionalidade
git push origin --delete feature/nova-funcionalidade
```

---

## 🐛 Debugging

### Django Debug Toolbar

```bash
# Instalar
pip install django-debug-toolbar

# settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
```

### Print Debugging

```python
# ✅ Bom
import logging

logger = logging.getLogger(__name__)

def product_create(request):
    logger.info(f"Criando produto para {request.user}")
    logger.debug(f"POST data: {request.POST}")
    
    # ... código ...
    
    logger.error(f"Erro ao criar produto", exc_info=True)
```

### Django Shell

```bash
python manage.py shell

# Interativo
>>> from products.models import Product
>>> products = Product.objects.all()
>>> for p in products:
...     print(p.name, p.price)

# Com IPython (melhor)
pip install ipython
python manage.py shell_plus
```

### Database Queries

```python
# Ver queries executadas
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:
    products = Product.objects.all()
    for p in products:
        print(p.name)

print(f"Queries executadas: {len(ctx.captured_queries)}")
for query in ctx.captured_queries:
    print(query['sql'])
```

---

## ⚡ Performance

### Otimizações Comuns

**1. Database Queries:**
```python
# ❌ N+1 queries
products = Product.objects.all()
for product in products:
    print(product.seller.company_name)  # Query por produto!

# ✅ select_related (FK/OneToOne)
products = Product.objects.select_related('seller').all()

# ✅ prefetch_related (M2M/reverse FK)
orders = Order.objects.prefetch_related('items').all()
```

**2. Pagination:**
```python
from django.core.paginator import Paginator

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)  # 12 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/list.html', {'page_obj': page_obj})
```

**3. Caching:**
```python
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@cache_page(60 * 5)  # Cache por 5 minutos
def product_list(request):
    return render(request, 'products/list.html')

# Ou manual:
def get_featured_products():
    products = cache.get('featured_products')
    if products is None:
        products = Product.objects.filter(featured=True)[:5]
        cache.set('featured_products', products, 60 * 60)  # 1 hora
    return products
```

**4. Database Indexing:**
```python
class Meta:
    indexes = [
        models.Index(fields=['seller', '-created_at']),
        models.Index(fields=['slug']),
    ]
```

---

## 📊 Monitoramento & Logs

### Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

---

## 📚 Recursos Adicionais

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/faq/design-philosophies/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

---

**Happy Coding! 🚀**
