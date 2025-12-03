# ✨ Boas Práticas - Solar Store

## 🎯 Código Limpo (Clean Code)

### 1. Nomes Significativos

```python
# ❌ Ruim
def get_data(x):
    temp = x * 2
    return temp

# ✅ Bom
def calculate_total_price(product_price):
    """Calcula preço total com impostos"""
    tax_multiplier = 2
    total = product_price * tax_multiplier
    return total
```

### 2. Funções Pequenas e Focadas

```python
# ❌ Ruim - Faz muita coisa
def create_order(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    cart = request.session.get('cart')
    if not cart:
        return redirect('cart')
    # ... mais 50 linhas
    return render(...)

# ✅ Bom - Responsabilidade única
def create_order(request):
    """Cria pedido do carrinho"""
    _verify_authentication(request)
    cart = _get_cart(request)
    order = _build_order(request.user, cart)
    return render(request, 'order_confirm.html', {'order': order})

def _verify_authentication(request):
    if not request.user.is_authenticated:
        raise PermissionDenied()

def _get_cart(request):
    cart = request.session.get('cart', {})
    if not cart:
        raise ValueError('Cart is empty')
    return cart
```

### 3. Evitar Magic Numbers

```python
# ❌ Ruim
def calculate_shipping(weight):
    if weight > 50:
        return 25.00
    return 10.00

# ✅ Bom
MAX_WEIGHT_FOR_STANDARD_SHIPPING = 50
STANDARD_SHIPPING_COST = 10.00
PREMIUM_SHIPPING_COST = 25.00

def calculate_shipping(weight):
    if weight > MAX_WEIGHT_FOR_STANDARD_SHIPPING:
        return PREMIUM_SHIPPING_COST
    return STANDARD_SHIPPING_COST
```

### 4. Comentários Significativos

```python
# ❌ Ruim
# Incrementar contador
counter += 1

# ✅ Bom
# Incrementar contador de tentativas falhas
# após 3 tentativas, bloquear usuário por 1 hora
failed_attempts += 1
```

### 5. DRY (Don't Repeat Yourself)

```python
# ❌ Ruim - Código repetido
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user.seller_profile)
    orders = Order.objects.filter(seller=request.user.seller_profile)
    # ...

def customer_dashboard(request):
    products = Product.objects.filter(owner=request.user.customer_profile)
    orders = Order.objects.filter(owner=request.user.customer_profile)
    # ...

# ✅ Bom - Usar mixins/herança
class UserDashboardView(LoginRequiredMixin):
    def get_user_profile(self):
        if hasattr(self.request.user, 'seller_profile'):
            return self.request.user.seller_profile
        return self.request.user.customer_profile
```

---

## 📐 Padrões Django

### 1. Usar Migrations Corretamente

```bash
# ✅ Bom workflow
python manage.py makemigrations  # Gera migração
python manage.py migrate         # Aplica no BD
```

```python
# ❌ Nunca fazer isso
# class Meta:
#     managed = False  # NÃO faça

# ✅ Sempre deixar como padrão
class Meta:
    managed = True
```

### 2. QuerySet Optimization

```python
# ❌ Ruim - múltiplas queries
for product in Product.objects.all():
    seller_name = product.seller.company_name  # Query por produto!

# ✅ Bom - select_related
products = Product.objects.select_related('seller')
for product in products:
    seller_name = product.seller.company_name  # Sem queries adicionais

# ✅ Bom - prefetch_related (M2M)
orders = Order.objects.prefetch_related('items')
for order in orders:
    for item in order.items.all():  # Sem queries adicionais
        pass
```

### 3. Usar Manager e QuerySet

```python
# ❌ Ruim - QuerySet na view
products = Product.objects.filter(is_active=True).filter(
    seller=seller
).order_by('-created_at')[:10]

# ✅ Bom - Manager customizado
class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def by_seller(self, seller):
        return self.filter(seller=seller)
    
    def recent(self, limit=10):
        return self.order_by('-created_at')[:limit]

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model)
    
    def active_by_seller(self, seller, limit=10):
        return self.get_queryset().active().by_seller(seller).recent(limit)

# Na view
products = Product.objects.active_by_seller(seller)
```

### 4. Validações em Modelos

```python
# ✅ Bom - validar no model
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def clean(self):
        if self.price < 0:
            raise ValidationError({'price': 'Preço não pode ser negativo'})
```

### 5. Use Django Forms para Validação

```python
# ✅ Bom - usar Django Forms
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 10:
            raise forms.ValidationError('Preço mínimo é R$ 10')
        return price

# Na view
form = ProductForm(request.POST)
if form.is_valid():
    form.save()  # Já valida
```

---

## 🔐 Segurança

### 1. Autenticação

```python
# ✅ Sempre verificar autenticação
from django.contrib.auth.decorators import login_required

@login_required
def product_edit(request):
    # Código protegido
    pass
```

### 2. Autorização

```python
# ✅ Verificar permissão
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Apenas o vendedor pode editar
    if product.seller.user != request.user:
        raise PermissionDenied()
    
    # Código protegido
    pass
```

### 3. CSRF Protection

```html
<!-- ✅ Sempre adicionar em forms -->
<form method="post">
    {% csrf_token %}
    <!-- campos do form -->
</form>
```

### 4. Validar Input do Usuário

```python
# ❌ Ruim - confia no usuário
user_id = request.GET.get('id')
product = Product.objects.get(id=user_id)

# ✅ Bom - validar
from django.shortcuts import get_object_or_404

product = get_object_or_404(Product, id=user_id)
```

### 5. Variáveis Sensíveis

```python
# ❌ Ruim - na versão
SECRET_KEY = 'minha-chave-secreta'
STRIPE_KEY = 'sk_live_...'

# ✅ Bom - em .env
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
STRIPE_KEY = os.getenv('STRIPE_SECRET_KEY')
```

---

## 📝 Documentação

### 1. Docstrings em Funções

```python
# ✅ Bom
def calculate_discount(price, discount_percent):
    """
    Calcula desconto no preço.
    
    Args:
        price (float): Preço original
        discount_percent (float): Percentual de desconto (0-100)
    
    Returns:
        float: Preço com desconto aplicado
    
    Raises:
        ValueError: Se discount_percent > 100
    """
    if discount_percent > 100:
        raise ValueError('Desconto não pode ser maior que 100%')
    return price * (1 - discount_percent / 100)
```

### 2. Docstrings em Classes

```python
# ✅ Bom
class Product(models.Model):
    """
    Modelo de produto no catálogo.
    
    Representa um item que pode ser vendido por um vendedor.
    Cada produto tem preço, estoque e imagem.
    
    Attributes:
        seller (FK): Vendedor que criou o produto
        name (str): Nome do produto
        price (Decimal): Preço em reais
        quantity (int): Quantidade em estoque
    """
    # ...
```

### 3. Comments Explicativos

```python
# ✅ Bom - explica o "por quê"
# Usar decimal em vez de float para evitar imprecisão
# em operações monetárias
price = models.DecimalField(max_digits=10, decimal_places=2)
```

---

## 🧪 Testes

### 1. Estrutura de Testes

```python
# ✅ Bom
class ProductModelTest(TestCase):
    """Testes do modelo Product"""
    
    def setUp(self):
        """Preparar dados para cada teste"""
        self.seller = create_seller()
        self.product = Product.objects.create(
            seller=self.seller,
            name='Test Product',
            price=100.00
        )
    
    def test_product_creation(self):
        """Testar criação de produto"""
        self.assertEqual(self.product.name, 'Test Product')
    
    def test_product_str(self):
        """Testar representação em string"""
        self.assertEqual(str(self.product), 'Test Product')
```

### 2. Cobertura de Casos

```python
# ✅ Bom - testar casos positivos e negativos
class ProductFormTest(TestCase):
    
    def test_form_valid(self):
        """Testar form com dados válidos"""
        form = ProductForm(data={
            'name': 'Product',
            'price': 100.00
        })
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_price(self):
        """Testar form com preço inválido"""
        form = ProductForm(data={
            'name': 'Product',
            'price': -10.00
        })
        self.assertFalse(form.is_valid())
```

---

## 🎨 CSS e Frontend

### 1. Usar Classes Significativas

```html
<!-- ❌ Ruim -->
<div class="red-box">
    <p class="title-p">Produto</p>
</div>

<!-- ✅ Bom -->
<div class="product-card">
    <h3 class="product-title">Produto</h3>
</div>
```

### 2. CSS Modular

```css
/* ✅ Bom - separar por componente */
/* components/button.css */
.btn {
    padding: 10px 20px;
    border: none;
    cursor: pointer;
}

.btn-primary {
    background: linear-gradient(135deg, #f7b733 0%, #fc4a1a 100%);
}

.btn-secondary {
    background: #003f7f;
}
```

### 3. Variáveis CSS

```css
/* ✅ Bom - reutilizar valores */
:root {
    --solar-yellow: #f7b733;
    --solar-orange: #fc4a1a;
    --solar-blue: #003f7f;
}

.btn-primary {
    background: linear-gradient(135deg, var(--solar-yellow) 0%, var(--solar-orange) 100%);
}
```

---

## 🔍 Linting e Formatting

### 1. PEP 8 Compliance

```bash
# Instalar flake8
pip install flake8

# Verificar código
flake8 products/views.py
```

### 2. Usar Black para Formatação

```bash
# Instalar black
pip install black

# Formatar arquivo
black products/views.py

# Formatar tudo
black .
```

### 3. Isort para Imports

```bash
# Instalar isort
pip install isort

# Organizar imports
isort products/views.py
```

---

## 📊 Performance

### 1. Indexar Campos Buscados

```python
# ✅ Bom - adicionar índice
class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['seller', '-created_at']),
        ]
```

### 2. Usar Cache

```python
# ✅ Bom - cachear dados

from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache por 5 minutos
def product_list(request):
    # Renderiza uma única vez, serve do cache
    pass
```

### 3. Lazy Loading

```python
# ✅ Bom - carregar sob demanda
class Product(models.Model):
    @property
    def has_reviews(self):
        """Verificar se tem reviews (lazy)"""
        return self.reviews.exists()
```

---

## 🚀 Deployment

### 1. Checklist Pré-Deploy

```markdown
- [ ] DEBUG=False
- [ ] SECRET_KEY forte
- [ ] ALLOWED_HOSTS configurado
- [ ] HTTPS/SSL
- [ ] Banco de dados produção
- [ ] Email configurado
- [ ] Static files coletados
- [ ] Logs configurados
- [ ] Monitoramento ativo
- [ ] Backup automated
```

### 2. Variáveis de Ambiente

```bash
# ✅ Bom - usar env vars
export DJANGO_SETTINGS_MODULE=solar_store.settings
export DEBUG=False
export SECRET_KEY=sua-chave-forte
```

---

## 🤝 Colaboração

### 1. Commits Significativos

```bash
# ❌ Ruim
git commit -m "fix"
git commit -m "updates"

# ✅ Bom
git commit -m "fix: corrigir validação de preço em checkout"
git commit -m "feat: adicionar sistema de reviews para produtos"
```

### 2. Pull Requests

```markdown
## Descrição
O que muda neste PR?

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change

## Testes
- [ ] Testes unitários
- [ ] Testes integração
- [ ] Teste manual

## Checklist
- [ ] Código formatado
- [ ] Documentação atualizada
- [ ] Sem TODOs pendentes
```

---

## 📚 Referências

- [Clean Code (Robert Martin)](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Django Best Practices](https://docs.djangoproject.com/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

## ✅ Checklist de Código

Antes de fazer commit:

- [ ] Código legível e bem nomeado
- [ ] Sem duplicação (DRY)
- [ ] Funcções pequenas e focadas
- [ ] Validações apropriadas
- [ ] Testes passando
- [ ] Documentação atualizada
- [ ] Sem variáveis sensíveis
- [ ] Formatted com black/isort
- [ ] Nenhum console.log ou print()
- [ ] Performance considerada

---

**Desenvolvido com excelência em mente! ☀️**
