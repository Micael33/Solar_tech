# 📡 API Reference - Views & URLs

## Estrutura de Endpoints

```
/                              → Home
/accounts/                     → Autenticação
/products/                     → Produtos
/cart/                         → Carrinho
/orders/                       → Pedidos
/payments/                     → Pagamentos
/admin/                        → Django Admin
```

---

## 🔐 Autenticação (accounts/)

### POST `/accounts/seller_register/`

**Descrição:** Registrar novo vendedor

**Parâmetros (Form Data):**
```json
{
  "username": "string",
  "email": "string",
  "password1": "string",
  "password2": "string",
  "first_name": "string",
  "last_name": "string",
  "cnpj": "string",
  "company_name": "string"
}
```

**Resposta:** Redireciona para login + mensagem "Registrado com sucesso!"

**Erros:**
- 400: Username já existe
- 400: Senhas não conferem
- 400: CNPJ inválido

---

### POST `/accounts/customer_register/`

**Descrição:** Registrar novo cliente

**Parâmetros (Form Data):**
```json
{
  "username": "string",
  "email": "string",
  "password1": "string",
  "password2": "string",
  "first_name": "string",
  "last_name": "string",
  "cpf": "string",
  "phone": "string",
  "address": "string"
}
```

**Resposta:** Login automático + Redireciona para customer_dashboard

**Erros:**
- 400: Username já existe
- 400: CPF já registrado

---

### POST `/accounts/login/`

**Descrição:** Realizar login

**Parâmetros (Form Data):**
```json
{
  "username": "string",
  "password": "string"
}
```

**Resposta:** 
```json
{
  "status": "success",
  "redirect": "/accounts/seller_dashboard/ ou /accounts/customer_dashboard/"
}
```

**Erros:**
- 401: Credenciais inválidas

---

### GET `/accounts/logout/`

**Descrição:** Realizar logout

**Autenticação:** Obrigatória

**Resposta:** Redireciona para home

---

### GET `/accounts/seller_dashboard/`

**Descrição:** Dashboard do vendedor

**Autenticação:** Obrigatória (vendedor)

**Resposta (Template):**
```html
<!-- Exibe:
  - Produtos do vendedor (listagem)
  - Botões: Novo Produto, Editar, Deletar
  - Pedidos recentes
  - Estatísticas (total de produtos, vendas)
-->
```

**Erros:**
- 403: Usuário não é vendedor

---

### GET `/accounts/customer_dashboard/`

**Descrição:** Dashboard do cliente

**Autenticação:** Obrigatória (cliente)

**Resposta (Template):**
```html
<!-- Exibe:
  - Informações do cliente
  - Pedidos recentes (tabela)
  - Estatísticas (total gasto, num pedidos)
  - Atalhos (Explorar Produtos, Carrinho, Meus Pedidos)
-->
```

**Erros:**
- 403: Usuário não é cliente

---

## 🛍️ Produtos (products/)

### GET `/products/`

**Descrição:** Listar todos os produtos (com busca)

**Parâmetros (Query String):**
```
?q=termo_busca
```

**Resposta (Template):**
```html
<!-- Exibe:
  - Produtos em grid (12 por página, opcional paginação)
  - Cards com imagem, nome, preço, botão "Ver Detalhes"
  - Search box
-->
```

---

### GET `/products/novo/`

**Descrição:** Formulário para criar novo produto

**Autenticação:** Obrigatória (vendedor)

**Resposta (Template):**
```html
<!-- Exibe formulário:
  - name
  - description
  - price
  - quantity
  - image (opcional)
  - image_url (opcional)
  - submit button
-->
```

**Erros:**
- 403: Usuário não é vendedor

---

### POST `/products/novo/`

**Descrição:** Criar novo produto

**Autenticação:** Obrigatória (vendedor)

**Parâmetros (Form Data):**
```json
{
  "name": "Painel Solar 500W",
  "description": "Descrição do produto",
  "price": "2500.00",
  "quantity": "10",
  "image": "file"
}
```

**Resposta:** Redireciona para product_detail

**Erros:**
- 400: Validação falhou
- 403: Usuário não é vendedor

---

### GET `/products/<slug>/`

**Descrição:** Detalhes de um produto

**URL Parameters:**
```
slug: string (ex: "painel-solar-500w")
```

**Resposta (Template):**
```json
{
  "product": {
    "id": 1,
    "name": "Painel Solar 500W",
    "price": "2500.00",
    "description": "Descrição completa",
    "quantity": 10,
    "seller": "SolarTech Brasil",
    "image": "url/to/image.jpg",
    "created_at": "2025-12-02T10:00:00Z"
  },
  "buttons": ["Adicionar ao Carrinho", "Editar (se vendedor)", "Deletar (se vendedor)"]
}
```

---

### GET `/products/<slug>/editar/`

**Descrição:** Formulário para editar produto

**Autenticação:** Obrigatória (vendedor + dono)

**URL Parameters:**
```
slug: string
```

**Resposta (Template):** Formulário pre-preenchido

**Erros:**
- 404: Produto não encontrado
- 403: Usuário não é dono do produto

---

### POST `/products/<slug>/editar/`

**Descrição:** Atualizar produto

**Autenticação:** Obrigatória (vendedor + dono)

**Parâmetros (Form Data):**
```json
{
  "name": "string",
  "description": "string",
  "price": "number",
  "quantity": "number",
  "image": "file (opcional)"
}
```

**Resposta:** Redireciona para product_detail

---

## 🛒 Carrinho (cart/)

### GET `/cart/`

**Descrição:** Exibir carrinho de compras

**Resposta (Template):**
```json
{
  "cart_items": [
    {
      "product": {
        "id": 1,
        "name": "Painel Solar 500W",
        "price": "2500.00",
        "image": "url"
      },
      "quantity": 2,
      "subtotal": 5000.00
    }
  ],
  "total": 5000.00,
  "buttons": ["Continuar Comprando", "Finalizar Compra"]
}
```

**Armazenamento:** Session-based (cookie)

---

### POST `/cart/add/` (se implementado)

**Descrição:** Adicionar item ao carrinho

**Parâmetros (AJAX):**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Resposta:**
```json
{
  "status": "success",
  "message": "Adicionado ao carrinho",
  "cart_count": 2
}
```

---

### POST `/cart/remove/` (se implementado)

**Descrição:** Remover item do carrinho

**Parâmetros:**
```json
{
  "product_id": 1
}
```

**Resposta:**
```json
{
  "status": "success",
  "message": "Removido do carrinho"
}
```

---

## 📦 Pedidos (orders/)

### GET `/orders/checkout/`

**Descrição:** Página de checkout

**Autenticação:** Obrigatória (cliente)

**Pré-requisitos:**
- Usuário logado como cliente
- Carrinho não vazio

**Resposta (Template):**
```json
{
  "order_summary": {
    "items": [
      {
        "product": "Painel Solar 500W",
        "quantity": 2,
        "price": 2500.00,
        "subtotal": 5000.00
      }
    ],
    "total": 5000.00
  },
  "form": {
    "fields": ["email", "address", "card_details (Stripe Elements)"]
  }
}
```

---

### POST `/orders/checkout/`

**Descrição:** Processar checkout (criar Order)

**Autenticação:** Obrigatória (cliente)

**Parâmetros (Form Data):**
```json
{
  "email": "cliente@example.com",
  "address": "Rua Solar, 123"
}
```

**Resposta:** 
```json
{
  "status": "created",
  "order_id": 1,
  "redirect": "/payments/create-session/"
}
```

**Errors:**
- 400: Carrinho vazio
- 400: Validação falhou
- 403: Não autenticado

---

### GET `/orders/`

**Descrição:** Listar pedidos do cliente

**Autenticação:** Obrigatória (cliente)

**Resposta (Template):**
```json
{
  "orders": [
    {
      "id": 1,
      "total": 5000.00,
      "status": "completed",
      "created_at": "2025-12-02T10:00:00Z",
      "items": ["Painel Solar 500W x2"]
    }
  ]
}
```

---

### GET `/orders/success/<order_id>/`

**Descrição:** Página de confirmação de pedido

**URL Parameters:**
```
order_id: integer
```

**Resposta (Template):**
```html
<!-- Exibe:
  - Número do pedido
  - Valor total
  - Items
  - Mensagem de sucesso
  - Botão para voltar ao dashboard
-->
```

---

## 💳 Pagamentos (payments/)

### POST `/payments/create-session/`

**Descrição:** Criar sessão de checkout do Stripe

**Autenticação:** Obrigatória

**Request (JSON):**
```json
{
  "order_id": 1
}
```

**Resposta:**
```json
{
  "status": "success",
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_..."
}
```

**Exemplo cURL:**
```bash
curl -X POST http://localhost:8000/payments/create-session/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1}'
```

---

### GET `/payments/success/`

**Descrição:** Callback após pagamento bem-sucedido

**Query Parameters:**
```
?session_id=cs_test_...
```

**Resposta:** Redireciona para /orders/success/<order_id>/

---

### GET `/payments/cancel/`

**Descrição:** Callback após cancelamento de pagamento

**Resposta:** Redireciona para /cart/ com mensagem

---

### POST `/payments/webhook/`

**Descrição:** Webhook Stripe para eventos

**Headers:**
```
Stripe-Signature: t=timestamp,v1=signature,...
```

**Body (JSON):**
```json
{
  "type": "charge.succeeded",
  "data": {
    "object": {
      "id": "ch_test_...",
      "metadata": {
        "session_id": "cs_test_..."
      }
    }
  }
}
```

**Resposta:**
```json
{
  "status": "success"
}
```

**Eventos Tratados:**
- `charge.succeeded` → Atualizar Payment status
- `charge.failed` → Registrar falha
- `charge.refunded` → Processar reembolso

---

## 🏠 Home (solar_store/)

### GET `/`

**Descrição:** Homepage

**Resposta (Template):**
```html
<!-- Exibe:
  - Hero section (call-to-action)
  - Featured products (produtos em destaque)
  - How it works (passo-a-passo)
  - Features (características)
  - Testimonials (opcional)
-->
```

---

### GET `/logout/`

**Descrição:** Logout do usuário

**Autenticação:** Obrigatória

**Resposta:** Redireciona para home

---

## 🔧 Admin Django

### GET `/admin/`

**Descrição:** Interface administrativa

**Autenticação:** Obrigatória (superuser)

**Funcionalidades:**
- Gerenciar Users
- Gerenciar SellerProfiles
- Gerenciar CustomerProfiles
- Gerenciar Products
- Gerenciar Orders
- Gerenciar Payments

---

## 📋 Status Codes & Erros

### Success Codes

```
200 OK              → Requisição bem-sucedida
201 Created         → Recurso criado
204 No Content      → Sucesso sem conteúdo
301/302 Redirect    → Redirecionamento
```

### Error Codes

```
400 Bad Request     → Validação falhou
401 Unauthorized    → Não autenticado
403 Forbidden       → Não autorizado
404 Not Found       → Recurso não encontrado
500 Server Error    → Erro no servidor
503 Service Down    → Serviço indisponível
```

---

## 🔒 Autenticação & Autorização

### Tipos de Autenticação

```python
@login_required  # Apenas usuários logados
def view(request):
    pass

def view_vendedor(request):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('home')
    # Código para vendedor

def view_cliente(request):
    if not hasattr(request.user, 'customer_profile'):
        return redirect('home')
    # Código para cliente
```

### Headers de Autenticação

```
# Django usa cookies de sessão
Cookie: sessionid=abc123def456...

# Ou em JSON:
Authorization: Bearer token_aqui
```

---

## 📊 Exemplo Completo - Fluxo de Compra

```bash
# 1. Registrar cliente
POST /accounts/customer_register/
  username=joao
  password1=senha123
  cpf=12345678900

# 2. Login
POST /accounts/login/
  username=joao
  password=senha123

# 3. Listar produtos
GET /products/

# 4. Ver detalhe
GET /products/painel-solar-500w/

# 5. Adicionar ao carrinho (JavaScript/Session)

# 6. Ver carrinho
GET /cart/

# 7. Checkout
GET /orders/checkout/
POST /orders/checkout/
  email=joao@example.com
  address=Rua Solar 123

# 8. Criar sessão Stripe
POST /payments/create-session/
  order_id=1

# 9. Redireciona para Stripe (externa)
# Cliente insere dados do cartão

# 10. Webhook Stripe notifica nosso servidor
# Status do pedido atualizado para "processing"

# 11. Cliente redirecionado para sucesso
GET /payments/success/?session_id=cs_test_...

# 12. Ver histórico de pedidos
GET /orders/
```

---

## 🧪 Testando com cURL

### Registrar Cliente
```bash
curl -X POST http://localhost:8000/accounts/customer_register/ \
  -d "username=test_user&email=test@example.com&password1=senha123&password2=senha123&cpf=12345678900&first_name=Test&last_name=User"
```

### Listar Produtos
```bash
curl http://localhost:8000/products/
```

### Buscar Produtos
```bash
curl "http://localhost:8000/products/?q=painel"
```

### Criar Sessão Stripe
```bash
curl -X POST http://localhost:8000/payments/create-session/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1}' \
  -b "sessionid=seu_session_id"
```

---

## 📚 Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [Stripe API Reference](https://stripe.com/docs/api)
- [REST API Best Practices](https://restfulapi.net/)

---

**Última atualização:** Dezembro 2025  
**Versão:** 1.0.0
