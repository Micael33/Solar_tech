# ☀️ Solar Store - E-commerce de Energia Solar

![Solar Tech Badge](https://img.shields.io/badge/Django-5.2.8-blue)
![Python Badge](https://img.shields.io/badge/Python-3.11+-green)
![Stripe Badge](https://img.shields.io/badge/Payment-Stripe-blueviolet)
![License Badge](https://img.shields.io/badge/License-MIT-brightgreen)

> Plataforma e-commerce moderna para comercializar produtos de energia solar com integração de pagamentos via Stripe.

## 📸 Screenshots

```
Homepage com Hero Section (tema solar)
↓
Catálogo de Produtos com Busca
↓
Detalhe do Produto com Adicionar ao Carrinho
↓
Carrinho com Revisão de Items
↓
Checkout com Stripe Payment
↓
Dashboard de Vendedor/Cliente
```

---

## ✨ Características Principais

### 👥 Sistema Dual de Usuários

- **Vendedores (Sellers)**
  - Registrar produtos
  - Editar/deletar produtos
  - Ver pedidos de clientes
  - Dashboard com estatísticas

- **Clientes (Customers)**
  - Navegar produtos
  - Carrinho de compras
  - Checkout com pagamento
  - Histórico de pedidos
  - Dashboard com perfil

### 🛍️ Catálogo de Produtos

- Busca e filtros
- Detalhes com imagem
- Suporte a múltiplos produtos por vendedor
- Upload de imagens com Pillow
- Validação de estoque

### 💳 Integração Stripe

- Checkout seguro com Stripe Elements
- Webhooks para eventos de pagamento
- Suporte a cartão de crédito
- Tratamento de erros de pagamento
- Confirmação por email

### 🎨 Design Profissional

- **Tema Visual "Energia Solar"**
  - Paleta harmônica (amarelo, laranja, azul)
  - Gradientes solares em CTA e botões
  - Interface responsiva
  - 8 arquivos CSS especializados

### 📊 Dashboards Inteligentes

- **Dashboard Vendedor:** Produtos, Pedidos, Estatísticas
- **Dashboard Cliente:** Perfil, Pedidos, Carrinho rápido
- Widgets com informações em tempo real

---

## 🏗️ Arquitetura Técnica

### Stack Tecnológico

```
Backend:        Django 5.2.8
Linguagem:      Python 3.11+
Banco Dados:    SQLite (Dev) / PostgreSQL (Prod)
Pagamentos:     Stripe 14.0.1
Imagens:        Pillow 12.0.0
Environment:    python-dotenv 1.2.1
Frontend:       HTML5 + CSS3 + JavaScript
```

### Arquitetura MVC

```
Models (apps/)
├── accounts/    User, SellerProfile, CustomerProfile
├── products/    Product
├── cart/        CartItem (session-based)
├── orders/      Order, OrderItem
└── payments/    Payment

Views (views.py em cada app)
├── Autenticação
├── CRUD de Produtos
├── Carrinho
├── Checkout
└── Pagamentos

URLs (urls.py)
├── /accounts/    → Autenticação
├── /products/    → Catálogo
├── /cart/        → Carrinho
├── /orders/      → Pedidos
└── /payments/    → Pagamentos
```

### Fluxo de Dados

```
Cliente → Browser → Django View → Models → SQLite
                        ↓
                    Template → HTML/CSS/JS
                        ↓
                     Browser (renderizado)
```

---

## 🚀 Getting Started

### Pré-requisitos

- Python 3.11+
- pip (gestor de pacotes)
- Conta Stripe (para pagamentos)
- Git

### Instalação Passo a Passo

#### 1. Clonar Repositório
```bash
git clone https://github.com/seu-usuario/solar-store.git
cd solar-store
```

#### 2. Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

#### 4. Configurar Variáveis de Ambiente
Criar `.env` na raiz:
```env
# Django
SECRET_KEY=generate-with-python-manage.py-shell
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe (teste)
STRIPE_PUBLIC_KEY=pk_test_seu_public_key
STRIPE_SECRET_KEY=sk_test_seu_secret_key
STRIPE_WEBHOOK_SECRET=whsec_seu_webhook_secret
```

#### 5. Aplicar Migrations
```bash
python manage.py migrate
```

#### 6. Criar Superuser (Admin)
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (sua senha)
```

#### 7. Rodar Servidor de Desenvolvimento
```bash
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000**

---

## 📚 Uso e Fluxo

### Para Clientes

1. **Registrar**
   ```
   Clique em "Registrar" → Escolha "Cliente" → Preencha CPF + dados
   ```

2. **Explorar Produtos**
   ```
   GET /products/ → Busque por termo
   ```

3. **Comprar Produto**
   ```
   Ver detalhe → Adicionar ao carrinho → Ir para carrinho → Checkout
   ```

4. **Pagar com Stripe**
   ```
   Inserir dados de cartão (teste: 4242 4242 4242 4242)
   ```

5. **Confirmar Pedido**
   ```
   Receber confirmação por email → Acessar historico em Dashboard
   ```

### Para Vendedores

1. **Registrar**
   ```
   Clique em "Registrar" → Escolha "Vendedor" → Preencha CNPJ
   ```

2. **Criar Produto**
   ```
   Dashboard → "Novo Produto" → Preencha nome, preço, descrição
   ```

3. **Gerenciar Produtos**
   ```
   Dashboard → Editar/Deletar produtos
   ```

4. **Ver Pedidos**
   ```
   Dashboard → Seção "Pedidos Recentes"
   ```

---

## 🎨 Design System

### Paleta de Cores Solar

| Nome | Hex | RGB | Uso |
|------|-----|-----|-----|
| Solar Yellow | `#f7b733` | 247, 183, 51 | Botões primários, accent |
| Solar Orange | `#fc4a1a` | 252, 74, 26 | CTA, preços, ações |
| Solar Blue | `#003f7f` | 0, 63, 127 | Headers, navbar |
| Blue Light | `#1976d2` | 25, 118, 210 | Gradients, secondary |
| Gray | `#6e6e6e` | 110, 110, 110 | Texto, labels |
| Light | `#fafafa` | 250, 250, 250 | Background |

### CSS Structure

```
base.css          → Estilos globais (navbar, buttons, forms, footer)
home.css          → Homepage (hero, features, CTA)
auth.css          → Autenticação (login, register forms)
products.css      → Catálogo (product-grid, cards, detail)
cart.css          → Carrinho (cart-table, summary, actions)
checkout.css      → Checkout (form, order-review, stripe)
orders.css        → Pedidos (order-list, status-badges, timeline)
dashboard.css     → Dashboards (stat-cards, action-buttons)
```

---

## 📖 Documentação Completa

Para mais detalhes, consulte:

- **[DOCUMENTATION.md](./DOCUMENTATION.md)** - Documentação técnica completa
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Referência rápida
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Arquitetura e modelos
- **[STRIPE_SETUP.md](./STRIPE_SETUP.md)** - Setup Stripe detalhado

---

## 🧪 Testando a Aplicação

### Criar Dados de Teste

```bash
python manage.py shell

# Criar vendedor
from django.contrib.auth.models import User
from accounts.models import SellerProfile

user = User.objects.create_user(
    username='seller',
    email='seller@test.com',
    password='123456'
)

SellerProfile.objects.create(
    user=user,
    cnpj='12345678000100',
    company_name='Solar Tech Brasil'
)

# Criar cliente
customer_user = User.objects.create_user(
    username='customer',
    email='customer@test.com',
    password='123456'
)

CustomerProfile.objects.create(
    user=customer_user,
    cpf='12345678900',
    phone='11999999999'
)

# Criar produto
from products.models import Product
from django.utils.text import slugify

Product.objects.create(
    seller=SellerProfile.objects.first(),
    name='Painel Solar 500W',
    slug=slugify('Painel Solar 500W'),
    description='Painel de alta eficiência',
    price=2500.00,
    quantity=10
)
```

### URLs de Teste

| URL | Método | Descrição |
|-----|--------|-----------|
| `/admin/` | GET | Admin Django |
| `/` | GET | Homepage |
| `/accounts/customer_register/` | GET/POST | Registro cliente |
| `/accounts/seller_register/` | GET/POST | Registro vendedor |
| `/accounts/login/` | GET/POST | Login |
| `/products/` | GET | Listar produtos |
| `/products/novo/` | GET/POST | Criar produto |
| `/products/<slug>/` | GET | Detalhe produto |
| `/products/<slug>/editar/` | GET/POST | Editar produto |
| `/cart/` | GET | Carrinho |
| `/orders/checkout/` | GET/POST | Checkout |
| `/payments/create-session/` | POST | Criar sessão Stripe |
| `/payments/success/` | GET | Sucesso pagamento |
| `/payments/cancel/` | GET | Cancelar pagamento |

### Dados de Teste - Stripe

**Cartão Válido (Teste):**
```
Número: 4242 4242 4242 4242
Data: 12/25 (qualquer data futura)
CVC: 123 (qualquer 3 dígitos)
```

**Cartão com Falha (Teste):**
```
Número: 4000 0000 0000 0002
Data: 12/25
CVC: 123
```

---

## 🔐 Segurança

### Boas Práticas Implementadas

- ✅ Senhas com hash (Django built-in)
- ✅ CSRF protection em formulários
- ✅ SQL Injection prevention (ORM Django)
- ✅ XSS prevention (template escaping)
- ✅ Authorization checks em views
- ✅ Secrets em .env (não commitados)
- ✅ Stripe API keys seguras
- ✅ Webhooks verificados

### Variáveis de Ambiente Obrigatórias

```env
SECRET_KEY          # Gerada automaticamente
DEBUG               # False em produção
ALLOWED_HOSTS       # Configurar em produção
STRIPE_PUBLIC_KEY   # De seu dashboard Stripe
STRIPE_SECRET_KEY   # De seu dashboard Stripe
```

---

## 📊 Estrutura de Dados

### User (Django Auth)
```python
id, username, email, password_hash, first_name, last_name, is_active, date_joined
```

### SellerProfile
```python
user (FK), cnpj, company_name, created_at
```

### CustomerProfile
```python
user (FK), cpf, phone, address, created_at
```

### Product
```python
seller (FK), name, slug, description, price, quantity, image, created_at, updated_at
```

### Order
```python
customer (FK), total, status, created_at, updated_at
```

### OrderItem
```python
order (FK), product (FK), quantity, price
```

### Payment
```python
order (FK), stripe_id, amount, status, created_at
```

---

## 🛠️ Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'stripe'"
```bash
pip install stripe==14.0.1
```

### Erro: "DEBUG must be False in production"
Verificar `.env`: `DEBUG=False`

### Erro: "No such table: products_product"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Stripe webhook não funciona
1. Verificar `STRIPE_WEBHOOK_SECRET` em `.env`
2. Configurar webhook em dashboard Stripe para `http://localhost:8000/payments/webhook/`
3. Testar com `stripe listen --forward-to localhost:8000/payments/webhook/`

### Imagens não aparecem
```bash
python manage.py collectstatic --noinput
```

---

## 📈 Performance

### Otimizações Implementadas

- ✅ CSS minificado
- ✅ Static files cacheados
- ✅ Database indexing
- ✅ Query optimization com select_related
- ✅ Pagination em listagens
- ✅ Lazy loading de imagens (futura)

---

## 🚀 Deployment

### Opções de Hosting

1. **Heroku**
   ```bash
   heroku login
   heroku create solar-store
   git push heroku main
   ```

2. **PythonAnywhere**
   - Simples upload via web
   - Banco PostgreSQL incluído

3. **DigitalOcean / Linode**
   - VPS com Ubuntu
   - Nginx + Gunicorn
   - SSL com Let's Encrypt

4. **AWS (EC2)**
   - Instância t3.micro (free tier)
   - RDS para PostgreSQL
   - S3 para static files

Ver `DEPLOYMENT.md` para guia completo.

---

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja `LICENSE` para mais detalhes.

---

## 👨‍💻 Autor

**Solar Tech Brasil**  
📧 Email: contato@solartech.com.br  
🌐 Website: https://www.solartech.com.br  

---

## 📞 Suporte

- 📖 [Documentação Completa](./DOCUMENTATION.md)
- 🐛 [Reportar Bug](https://github.com/seu-usuario/solar-store/issues)
- 💡 [Sugerir Feature](https://github.com/seu-usuario/solar-store/issues)
- 💬 [Discussões](https://github.com/seu-usuario/solar-store/discussions)

---

## 🙏 Agradecimentos

- Django team pelo framework incrível
- Stripe pela integração de pagamentos
- Comunidade Python/Django
- Contribuidores do projeto

---

## 📅 Changelog

### v1.0.0 (Dezembro 2025)
- ✨ Lançamento inicial
- 👥 Sistema de autenticação dual (Seller/Customer)
- 🛍️ Catálogo de produtos
- 🛒 Carrinho de compras
- 💳 Integração Stripe
- 🎨 Design system com tema Solar
- 📊 Dashboards com estatísticas

---

**Desenvolvido com ❤️ e ☀️**

Vamos iluminar o futuro da energia solar! 🌞
