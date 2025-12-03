# 🚀 Quick Start - Solar Store

## Instalação Rápida (5 minutos)

### 1️⃣ Clonar e Configurar Ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2️⃣ Configurar Variáveis de Ambiente

Criar `.env` na raiz:
```
SECRET_KEY=seu-secret-key-aqui
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### 3️⃣ Setup do Banco de Dados

```bash
# Aplicar migrations
python manage.py migrate

# Criar superuser
python manage.py createsuperuser
```

### 4️⃣ Rodar Servidor

```bash
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000`

---

## 👤 Criar Usuários de Teste

### Vendedor

```bash
# No shell Django
python manage.py shell

from django.contrib.auth.models import User
from accounts.models import SellerProfile

user = User.objects.create_user(
    username='seller1',
    email='seller@test.com',
    password='123456'
)

SellerProfile.objects.create(
    user=user,
    cnpj='12345678000100',
    company_name='SolarTech Brasil'
)
```

### Cliente

```bash
from django.contrib.auth.models import User
from accounts.models import CustomerProfile

user = User.objects.create_user(
    username='customer1',
    email='customer@test.com',
    password='123456'
)

CustomerProfile.objects.create(
    user=user,
    cpf='12345678900',
    phone='11999999999',
    address='Rua Solar, 123'
)
```

---

## 📱 Fluxo de Teste

### 1. Registrar Novo Cliente
```
GET /accounts/customer_register/
Preencher formulário → POST
Será redirecionado para login
```

### 2. Login
```
GET /accounts/login/
username: customer1
password: 123456
```

### 3. Explorar Produtos
```
GET /products/
Buscar por termo (ex: "painel")
```

### 4. Detalhe do Produto
```
GET /products/painel-solar-500w/
Adicionar ao carrinho
```

### 5. Carrinho
```
GET /cart/
Revisar items
Clique "Finalizar Compra"
```

### 6. Checkout
```
GET /orders/checkout/
Preencher dados
Clique "Ir para Pagamento"
(será redirecionado para Stripe)
```

---

## 🎨 Paleta de Cores (Solar Theme)

| Cor | Hex | Uso |
|-----|-----|-----|
| Amarelo Solar | `#f7b733` | Buttons, Accent |
| Laranja Solar | `#fc4a1a` | CTA, Prices |
| Azul Solar | `#003f7f` | Headers, Navbar |
| Azul Claro | `#1976d2` | Gradients |
| Cinza | `#6e6e6e` | Text |
| Branco | `#fafafa` | Background |

---

## 📁 Estrutura Principal

```
accounts/      → Autenticação (seller, customer)
products/      → Catálogo de produtos
cart/          → Carrinho de compras
orders/        → Pedidos e checkout
payments/      → Stripe integration
static/css/    → Estilos (8 arquivos)
templates/     → HTML
```

---

## ⚡ Comandos Úteis

```bash
# Criar migrations
python manage.py makemigrations

# Listar apps
python manage.py show_apps

# Shell Django
python manage.py shell

# Verificar sistema
python manage.py check

# Exports statics
python manage.py collectstatic

# Teste de cobertura
coverage run --source='.' manage.py test
coverage report
```

---

## 🔗 URLs Principais

| URL | Descrição |
|-----|-----------|
| `/` | Homepage |
| `/accounts/customer_register/` | Registro Cliente |
| `/accounts/seller_register/` | Registro Vendedor |
| `/accounts/login/` | Login |
| `/accounts/customer_dashboard/` | Dashboard Cliente |
| `/accounts/seller_dashboard/` | Dashboard Vendedor |
| `/products/` | Catálogo |
| `/products/novo/` | Criar Produto |
| `/cart/` | Carrinho |
| `/orders/checkout/` | Checkout |
| `/admin/` | Admin (Django) |

---

## 💳 Testando Stripe

### Dados de Teste (Sandbox)

**Cartão Válido:**
```
4242 4242 4242 4242
MM/YY: Qualquer data futura
CVC: Qualquer 3 dígitos
```

**Cartão com Falha:**
```
4000 0000 0000 0002
MM/YY: Qualquer data futura
CVC: Qualquer 3 dígitos
```

---

## 📖 Documentação Completa

Veja `DOCUMENTATION.md` para:
- Arquitetura completa
- Diagramas ER
- Fluxos de negócio
- Exemplos de código
- Guia de deployment

---

**Pronto para começar? Rode `python manage.py runserver` e acesse `http://127.0.0.1:8000` 🚀**
