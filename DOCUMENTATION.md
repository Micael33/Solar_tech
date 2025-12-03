# 📚 Documentação Completa - Solar Store

**Versão:** 1.0  
**Data:** Dezembro 2025  
**Linguagem:** Python (Django 5.2.8)  
**Banco de Dados:** SQLite3

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Requisitos do Projeto](#requisitos-do-projeto)
3. [Estrutura de Diretórios](#estrutura-de-diretórios)
4. [Instalação e Setup](#instalação-e-setup)
5. [Arquitetura de Banco de Dados](#arquitetura-de-banco-de-dados)
6. [Autenticação e Autorização](#autenticação-e-autorização)
7. [Aplicações Django](#aplicações-django)
8. [Sistema de Pagamentos](#sistema-de-pagamentos)
9. [Frontend e Design](#frontend-e-design)
10. [Fluxogramas de Negócio](#fluxogramas-de-negócio)
11. [Exemplos de Código](#exemplos-de-código)
12. [Deployment e Produção](#deployment-e-produção)

---

## 🎯 Visão Geral

**Solar Store** é uma plataforma e-commerce moderna desenvolvida com Django que conecta **vendedores** (provedores de tecnologia solar) com **clientes** (compradores). 

### Características principais:

- ✅ Autenticação de dois tipos de usuários (Seller e Customer)
- ✅ Catálogo de produtos com busca e filtros
- ✅ Carrinho de compras persistente
- ✅ Integração com Stripe para pagamentos seguros
- ✅ Dashboard para vendedores e clientes
- ✅ Gestão de pedidos e histórico
- ✅ Tema visual "Energia Solar" com paleta de cores harmônica
- ✅ Responsivo (mobile, tablet, desktop)

---

## 📦 Requisitos do Projeto

### Dependências:

```
Django==5.2.8                # Framework web
Pillow==12.0.0              # Processamento de imagens
Stripe==14.0.1              # API de pagamentos
python-dotenv==1.2.1        # Variáveis de ambiente
requests==2.32.5            # Requisições HTTP
asgiref==3.11.0             # Suporte ASGI
sqlparse==0.5.3             # Parser SQL
tzdata==2025.2              # Dados de timezone
```

### Requisitos do Sistema:

- Python 3.11+
- pip (gestor de pacotes)
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Conexão com internet (para Stripe)

### Instalação de Dependências:

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
# Criar arquivo .env na raiz do projeto com:
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

---

## 📁 Estrutura de Diretórios

```
Solar_Tech/
├── solar_store/                  # Configuração principal do Django
│   ├── settings.py              # Configurações globais
│   ├── urls.py                  # Roteamento principal
│   ├── wsgi.py                  # WSGI para produção
│   ├── asgi.py                  # ASGI para async
│   └── views.py                 # Views globais (home, logout)
│
├── accounts/                     # App de autenticação
│   ├── models.py                # SellerProfile, CustomerProfile
│   ├── views.py                 # Registro, login, dashboards
│   ├── forms.py                 # Formulários de autenticação
│   ├── urls.py                  # URLs de accounts
│   └── templates/
│       ├── customer_dashboard.html
│       ├── seller_dashboard.html
│       ├── customer_register.html
│       └── seller_register.html
│
├── products/                     # App de produtos
│   ├── models.py                # Modelo Product
│   ├── views.py                 # CRUD de produtos
│   ├── forms.py                 # ProductForm
│   ├── urls.py                  # URLs de produtos
│   └── templates/products/
│       ├── product_list.html
│       ├── product_detail.html
│       └── product_form.html
│
├── cart/                         # App de carrinho
│   ├── models.py                # CartItem (se persistente)
│   ├── views.py                 # Exibir carrinho
│   ├── urls.py                  # URLs de carrinho
│   └── templates/cart/
│       └── cart_detail.html
│
├── orders/                       # App de pedidos
│   ├── models.py                # Order, OrderItem
│   ├── views.py                 # Criar pedido, listar pedidos
│   ├── urls.py                  # URLs de pedidos
│   └── templates/orders/
│       ├── checkout.html
│       ├── order_list.html
│       └── order_success.html
│
├── payments/                     # App de pagamentos
│   ├── models.py                # Payment
│   ├── views.py                 # Stripe session, webhooks
│   ├── urls.py                  # URLs de pagamentos
│   └── webhooks.py              # Tratamento de eventos Stripe
│
├── static/                       # Arquivos estáticos
│   ├── css/                     # Folhas de estilo
│   │   ├── base.css             # Estilos globais + paleta solar
│   │   ├── home.css             # Homepage
│   │   ├── auth.css             # Autenticação
│   │   ├── products.css         # Produtos
│   │   ├── cart.css             # Carrinho
│   │   ├── checkout.css         # Checkout
│   │   ├── orders.css           # Pedidos
│   │   └── dashboard.css        # Dashboards
│   ├── js/                      # JavaScript (se houver)
│   └── media/                   # Upload de imagens de produtos
│
├── templates/                    # Templates globais
│   ├── base/
│   │   └── base.html            # Template base (herança)
│   ├── home.html                # Homepage
│   ├── registration/            # Templates de auth padrão Django
│   │   ├── login.html
│   │   ├── logout.html
│   │   └── password_reset_*.html
│   ├── orders/
│   │   ├── checkout.html
│   │   ├── order_list.html
│   │   └── order_success.html
│   └── cart/
│       └── cart_detail.html
│
├── manage.py                     # CLI do Django
├── requirements.txt              # Dependências do projeto
├── db.sqlite3                    # Banco de dados (desenvolvimento)
├── .env                          # Variáveis de ambiente (git-ignored)
├── .gitignore                    # Arquivos ignorados pelo Git
└── README.md                     # Este arquivo
```

---

## 🗄️ Arquitetura de Banco de Dados

### Diagrama ER (Entity-Relationship):

```
┌─────────────────┐
│     User        │ (Django built-in)
│  (Django Auth)  │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ password        │
│ first_name      │
│ last_name       │
│ is_active       │
└────────┬────────┘
         │ 1:1
    ┌────┴──────────────────┐
    │                       │
    ▼                       ▼
┌──────────────┐    ┌──────────────────┐
│ SellerProfile│    │ CustomerProfile  │
├──────────────┤    ├──────────────────┤
│ user (FK)    │    │ user (FK)        │
│ cnpj         │    │ cpf              │
│ company_name │    │ phone            │
│ created_at   │    │ address          │
└──────┬───────┘    │ created_at       │
       │            └──────────────────┘
       │ 1:M
       ▼
┌──────────────┐
│   Product    │
├──────────────┤
│ id (PK)      │
│ seller (FK)  │ ────► SellerProfile
│ name         │
│ slug         │
│ description  │
│ price        │
│ quantity     │
│ image        │
│ created_at   │
│ updated_at   │
└──────┬───────┘
       │ 1:M
       ▼
┌──────────────────┐
│    CartItem      │ (Session-based ou DB)
├──────────────────┤
│ product (FK)     │
│ quantity         │
│ added_at         │
└──────────────────┘

┌──────────────┐
│    Order     │
├──────────────┤
│ id (PK)      │
│ customer (FK)│ ────► CustomerProfile
│ total        │
│ status       │ (pending, processing, completed)
│ created_at   │
│ updated_at   │
└──────┬───────┘
       │ 1:M
       ▼
┌──────────────────┐
│   OrderItem      │
├──────────────────┤
│ id (PK)          │
│ order (FK)       │
│ product (FK)     │
│ quantity         │
│ price           │
└──────────────────┘

┌──────────────┐
│   Payment    │
├──────────────┤
│ id (PK)      │
│ order (FK)   │ ────► Order (1:1)
│ stripe_id    │
│ amount       │
│ status       │ (pending, succeeded, failed)
│ created_at   │
└──────────────┘
```

### Modelos Django:

#### 1. **SellerProfile** (accounts/models.py)
```python
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    cnpj = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company_name} ({self.user.username})"
```

#### 2. **CustomerProfile** (accounts/models.py)
```python
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    cpf = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.username})"
```

#### 3. **Product** (products/models.py)
```python
class Product(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
```

#### 4. **Order** (orders/models.py)
```python
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
    ]
    
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.customer.user.username}"
    
    class Meta:
        ordering = ['-created_at']
```

#### 5. **OrderItem** (orders/models.py)
```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
```

#### 6. **Payment** (payments/models.py)
```python
class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('succeeded', 'Sucesso'),
        ('failed', 'Falha'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    stripe_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Pagamento #{self.id} - {self.status}"
```

---

## 🔐 Autenticação e Autorização

### Fluxo de Registro:

```
┌─────────────────────────────────────┐
│   Usuário acessa /accounts/         │
│   register e escolhe tipo           │
└────────────┬────────────────────────┘
             │
     ┌───────┴──────────┐
     │                  │
     ▼                  ▼
┌────────────┐  ┌──────────────┐
│ Vendedor?  │  │  Cliente?    │
│            │  │              │
└────┬───────┘  └──────┬───────┘
     │                 │
     ▼                 ▼
┌────────────────────────────────┐
│ Preenchir dados + CNPJ/CPF     │
│ (formulário validado)          │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│ Enviar POST a seller_register  │
│ ou customer_register           │
└────────┬───────────────────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
 Válido?   Inválido?
    │          │
    ▼          ▼
 Criar    Retornar erros
 User +   + form para
 Profile  reenviar
    │
    ▼
┌────────────────────────────────┐
│ Criar novo User (Django Auth)  │
│ + SellerProfile / CustomerProfile
│ + Salvar no banco              │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│ Redirecionar para login        │
│ "Registrado com sucesso!"      │
└────────────────────────────────┘
```

### Fluxo de Login:

```
┌──────────────────────┐
│ POST /accounts/login │
├──────────────────────┤
│ username             │
│ password             │
└─────────┬────────────┘
          │
          ▼
┌─────────────────────────────┐
│ Validar credenciais         │
│ authenticate(username, pwd) │
└─────────┬───────────────────┘
          │
      ┌───┴───┐
      │       │
      ▼       ▼
   Válido   Inválido
      │       │
      ▼       ▼
   Criar   Erro 401
   Session (re-render form)
   Login
      │
      ▼
   Redirecionar para
   - /accounts/seller_dashboard
   - /accounts/customer_dashboard
   (dependendo do perfil)
```

### Código de Exemplo - Registro de Cliente:

```python
# accounts/views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import CustomerProfile
from .forms import CustomerRegisterForm

def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            # Criar usuário Django
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # Criar perfil de cliente
            customer_profile = CustomerProfile.objects.create(
                user=user,
                cpf=form.cleaned_data['cpf'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            
            # Login automático
            login(request, user)
            
            messages.success(request, 'Bem-vindo! Você está registrado e logado.')
            return redirect('customer_dashboard')
    else:
        form = CustomerRegisterForm()
    
    return render(request, 'accounts/customer_register.html', {'form': form})
```

---

## 🛒 Aplicações Django

### 1. **accounts** - Autenticação e Perfis

**Arquivo:** `accounts/models.py`  
**Responsabilidade:** Gerenciar usuários, perfis de vendedores e clientes

**Views Principais:**
- `seller_register` — Registro de vendedores
- `customer_register` — Registro de clientes
- `seller_dashboard` — Dashboard do vendedor
- `customer_dashboard` — Dashboard do cliente
- `logout_view` — Logout

**URLs:**
```python
path('seller_register/', views.seller_register, name='seller_register')
path('customer_register/', views.customer_register, name='customer_register')
path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard')
path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard')
```

### 2. **products** - Catálogo de Produtos

**Arquivo:** `products/models.py`  
**Responsabilidade:** Gerenciar produtos, CRUD completo para vendedores

**Views Principais:**
- `product_list` — Listar todos os produtos (com busca)
- `product_detail` — Detalhe de um produto
- `product_create` — Criar novo produto (vendedor)
- `product_edit` — Editar produto (vendedor, com autorização)

**URLs:**
```python
path('', views.product_list, name='product_list')
path('novo/', views.product_create, name='product_create')
path('<slug:slug>/', views.product_detail, name='product_detail')
path('<slug:slug>/editar/', views.product_edit, name='product_edit')
```

**Exemplo - Listar Produtos:**
```python
# products/views.py
from django.shortcuts import render
from .models import Product

def product_list(request):
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(
            name__icontains=query
        ) | Product.objects.filter(
            description__icontains=query
        )
    else:
        products = Product.objects.all()
    
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'products/product_list.html', context)
```

### 3. **cart** - Carrinho de Compras

**Responsabilidade:** Gerenciar carrinho (session-based)

**Views Principais:**
- `cart_detail` — Exibir carrinho

**Implementação:**
```python
# cart/views.py
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = float(product.price) * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
        except Product.DoesNotExist:
            pass
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'cart/cart_detail.html', context)
```

### 4. **orders** - Pedidos e Checkout

**Responsabilidade:** Gerenciar pedidos, checkout e histórico

**Views Principais:**
- `checkout` — Página de checkout
- `order_list` — Histórico de pedidos
- `order_success` — Confirmação de pedido

**Fluxo de Checkout:**
```
┌──────────────────┐
│ GET /orders/     │
│ checkout/        │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ Verificar:           │
│ - Usuário logado?    │
│ - Carrinho não vazio?│
└────────┬─────────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
 OK        Erro
    │          │
    ▼          ▼
 Exibir  Redirecionar
 Form    /cart/
 (Dados
  Cliente
  + Stripe)
    │
    ▼
┌──────────────────┐
│ POST /orders/    │
│ checkout/        │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ Criar Order          │
│ + OrderItems         │
│ (cada item do       │
│  carrinho)          │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Enviar para Stripe   │
│ (criar Checkout      │
│  Session)            │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Redirecionar para    │
│ Stripe (pagamento)   │
└──────────────────────┘
```

### 5. **payments** - Integração Stripe

**Responsabilidade:** Gerenciar pagamentos com Stripe, webhooks

**Views Principais:**
- `create_checkout_session` — Criar sessão de pagamento
- `payment_success` — Callback após sucesso
- `payment_cancel` — Callback após cancelamento
- `stripe_webhook` — Webhook de eventos Stripe

**Integração Stripe:**
```python
# payments/views.py
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    if request.method != 'POST':
        return redirect('cart_detail')
    
    # Recuperar carrinho da sessão
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('product_list')
    
    # Criar Order
    order = Order.objects.create(
        customer=request.user.customer_profile,
        total=0  # Será calculado
    )
    
    # Preparar items para Stripe
    line_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        
        # Criar OrderItem
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        
        # Adicionar ao Stripe
        line_items.append({
            'price_data': {
                'currency': 'brl',
                'product_data': {
                    'name': product.name,
                    'images': [product.image_url or '']
                },
                'unit_amount': int(product.price * 100)
            },
            'quantity': quantity
        })
        
        total += float(product.price) * quantity
    
    # Atualizar total do pedido
    order.total = total
    order.save()
    
    # Criar Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=f"{request.build_absolute_uri('/payments/success/')}{order.id}/",
        cancel_url=request.build_absolute_uri('/payments/cancel/'),
        customer_email=request.user.email
    )
    
    return redirect(session.url)
```

---

## 💳 Sistema de Pagamentos

### Fluxo Completo de Pagamento:

```
┌─────────────────────────────────┐
│ Cliente clica "Finalizar Compra"│
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ POST /payments/create-session/  │
│ (backend cria Order + OrderItems)
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Stripe.checkout.Session.create()│
│ (retorna URL de checkout)       │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Redirecionar para Stripe        │
│ (página de pagamento do Stripe) │
└────────┬────────────────────────┘
         │
         ▼
    ┌────┴─────┐
    │           │
    ▼           ▼
Pagamento   Pagamento
  OK        CANCELADO
    │           │
    ▼           ▼
Callback   Callback
success/   cancel/
    │           │
    ▼           ▼
Webhook: ──► Atualizar
charge.     Status Order
succeeded   (cancelled)
    │
    ▼
Criar Payment
(status=succeeded)
Limpar carrinho
Enviar email
Redirecionar para
order_success
```

### Webhook Stripe:

```python
# payments/webhooks.py
from django.views.decorators.http import csrf_exempt
from django.http import JsonResponse
import stripe

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Tratamento de eventos
    if event['type'] == 'charge.succeeded':
        session_id = event['data']['object']['metadata']['session_id']
        
        # Encontrar Order e marcar como paga
        payment = Payment.objects.get(stripe_id=session_id)
        payment.status = 'succeeded'
        payment.save()
        
        payment.order.status = 'processing'
        payment.order.save()
    
    elif event['type'] == 'charge.failed':
        # Atualizar status de falha
        pass
    
    return JsonResponse({'status': 'success'})
```

---

## 🎨 Frontend e Design

### Paleta de Cores Solar (tema.css):

```css
:root {
    --solar-yellow: #f7b733;      /* Amarelo brilhante */
    --solar-orange: #fc4a1a;      /* Laranja quente */
    --solar-blue: #003f7f;        /* Azul profundo */
    --solar-blue-light: #1976d2;  /* Azul tecnológico */
    --solar-gray: #6e6e6e;        /* Cinza grafite */
    --solar-light: #fafafa;       /* Branco quase-puro */
}
```

### Estrutura de CSS:

```
static/css/
├── base.css          # Estilos globais, navbar, botões, formulários
├── home.css          # Homepage, hero, features, CTA
├── auth.css          # Autenticação (login, registro)
├── products.css      # Listagem e detalhe de produtos
├── cart.css          # Carrinho de compras
├── checkout.css      # Página de checkout
├── orders.css        # Histórico de pedidos
└── dashboard.css     # Dashboards (vendedor + cliente)
```

### Template Base (herança):

```html
<!-- templates/base/base.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Solar Store{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/base.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="navbar-container">
            <a href="{% url 'home' %}" class="navbar-brand">☀️ Solar Store</a>
            <ul class="navbar-nav">
                {% if user.is_authenticated %}
                    <li><a href="{% url 'product_list' %}">Produtos</a></li>
                    <li><a href="{% url 'cart_detail' %}">🛒 Carrinho</a></li>
                    {% if user.seller_profile %}
                        <li><a href="{% url 'seller_dashboard' %}">Dashboard</a></li>
                    {% elif user.customer_profile %}
                        <li><a href="{% url 'customer_dashboard' %}">Dashboard</a></li>
                    {% endif %}
                    <li><a href="{% url 'logout' %}">Sair</a></li>
                {% else %}
                    <li><a href="{% url 'login' %}">Login</a></li>
                {% endif %}
            </ul>
        </div>
    </nav>
    
    <!-- Container Principal -->
    <div class="container">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>
    
    <!-- Footer -->
    <footer>
        <p>&copy; 2025 Solar Store. Todos os direitos reservados.</p>
    </footer>
</body>
</html>
```

---

## 📊 Fluxogramas de Negócio

### Fluxo Principal de Compra:

```
┌────────────────────┐
│  Visitante Chega   │
│  na Homepage       │
└────────┬───────────┘
         │
         ▼
    ┌────────────┐
    │ Logado?    │
    └─┬──────┬──┘
      │ Não  │ Sim
      ▼      ▼
    Login  Dashboard
  Register  (Perfil)
      │      │
      ▼      ▼
    ┌─────────────────┐
    │ Explorar        │
    │ Produtos        │
    │ /products/      │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Ver Detalhe     │
    │ /products/<id>/ │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Adicionar ao    │
    │ Carrinho        │
    │ (session)       │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Ir para         │
    │ /cart/          │
    │ (revisar items) │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Checkout        │
    │ /orders/        │
    │ checkout/       │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Stripe Payment  │
    │ (externo)       │
    └────────┬────────┘
             │
        ┌────┴───┐
        │         │
        ▼         ▼
     Success   Cancel
        │         │
        ▼         ▼
    Webhook  Redirect
    Atualiza /payments/
    Status   cancel/
        │
        ▼
    ┌─────────────────┐
    │ Order Created   │
    │ Status:         │
    │ processing      │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Email enviado   │
    │ /orders/success │
    │ /<order_id>/    │
    └─────────────────┘
```

### Fluxo de Vendedor:

```
┌─────────────────────┐
│ Vendedor registrado │
│ /seller_register/   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Dashboard Vendedor  │
│ Ver produtos        │
│ Ver pedidos         │
└────────┬────────────┘
         │
    ┌────┼────┐
    │    │    │
    ▼    ▼    ▼
  Novo Editar Deletar
  Prod  Prod  Prod
    │    │    │
    ▼    ▼    ▼
   /novo/ /<slug>/
            editar/
           (com auth)
```

---

## 💻 Exemplos de Código

### Exemplo 1: Criar Produto (Vendedor)

```python
# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from .forms import ProductForm

@login_required
def product_create(request):
    # Verificar se usuário é vendedor
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, 'Apenas vendedores podem criar produtos.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.save()
            
            messages.success(request, 'Produto criado com sucesso!')
            return redirect('product_detail', slug=product.slug)
    else:
        form = ProductForm()
    
    context = {'form': form}
    return render(request, 'products/product_form.html', context)
```

### Exemplo 2: Editar Produto (com Autorização)

```python
# products/views.py
@login_required
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Verificar se vendedor é dono do produto
    if product.seller.user != request.user:
        messages.error(request, 'Você não tem permissão para editar este produto.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product': product}
    return render(request, 'products/product_form.html', context)
```

### Exemplo 3: Dashboard Cliente (com Estatísticas)

```python
# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order

@login_required
def customer_dashboard(request):
    # Verificar se é cliente
    if not hasattr(request.user, 'customer_profile'):
        return redirect('home')
    
    customer = request.user.customer_profile
    
    # Estatísticas
    orders = Order.objects.filter(customer=customer)
    total_orders = orders.count()
    total_spent = sum(order.total for order in orders) if orders.exists() else 0
    
    # Carrinho
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if cart else 0
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'cart_count': cart_count
    }
    
    return render(request, 'accounts/customer_dashboard.html', context)
```

### Exemplo 4: Busca de Produtos

```python
# products/views.py
def product_list(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        # Busca em nome e descrição
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        ).order_by('-created_at')
    else:
        products = Product.objects.all().order_by('-created_at')
    
    # Paginação (opcional)
    from django.core.paginator import Paginator
    paginator = Paginator(products, 12)  # 12 produtos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'query': query
    }
    
    return render(request, 'products/product_list.html', context)
```

---

## 🚀 Deployment e Produção

### Checklist de Deployment:

```markdown
## Pre-Deployment

- [ ] Executar `python manage.py check --deploy`
- [ ] Verificar todas as variáveis de ambiente (.env)
- [ ] Configurar `DEBUG = False` em settings.py
- [ ] Gerar nova `SECRET_KEY`
- [ ] Configurar `ALLOWED_HOSTS`
- [ ] Executar `collectstatic` para static files
- [ ] Testar banco de dados (migrations)

## Deployment Steps

1. **Configurar ambiente**
   ```bash
   export DJANGO_SETTINGS_MODULE=solar_store.settings
   export DEBUG=False
   export ALLOWED_HOSTS=example.com,www.example.com
   ```

2. **Executar migrations**
   ```bash
   python manage.py migrate
   ```

3. **Coletar static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Criar superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Usar WSGI server** (ex: Gunicorn)
   ```bash
   pip install gunicorn
   gunicorn solar_store.wsgi:application --bind 0.0.0.0:8000
   ```

6. **Configurar Nginx como reverse proxy**
   ```nginx
   server {
       listen 80;
       server_name example.com;
       
       location /static/ {
           alias /path/to/static/;
       }
       
       location /media/ {
           alias /path/to/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

7. **SSL/HTTPS com Let's Encrypt**
   ```bash
   pip install certbot-nginx
   certbot --nginx -d example.com
   ```

## Post-Deployment

- [ ] Monitorar logs
- [ ] Configurar backup de banco de dados
- [ ] Testar pagamentos Stripe em produção
- [ ] Configurar email transacional
- [ ] Monitorar performance e uptime
```

### Variáveis de Ambiente (.env):

```
# Django
SECRET_KEY=generate-with-get_random_secret_key()
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Stripe
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app
```

---

## 📝 Conclusão

Este documento fornece uma visão completa do projeto **Solar Store**, incluindo:

✅ Arquitetura de banco de dados  
✅ Fluxos de autenticação e autorização  
✅ Integração de pagamentos (Stripe)  
✅ Exemplos de código práticos  
✅ Guia de deployment  
✅ Paleta de cores e design  

Para questões adicionais ou contribuições, consulte o arquivo `CONTRIBUTING.md` ou abra uma issue no GitHub.

---

**Desenvolvido com ❤️ e ☀️ em 2025**
