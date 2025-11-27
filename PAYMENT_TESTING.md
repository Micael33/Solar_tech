# Guia de Teste do Sistema de Pagamento

## 🧪 Teste Rápido (Modo Desenvolvimento)

### 1. Iniciar o Servidor

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

### 2. Criar um Usuário Cliente (Teste)

Opção A - Via Admin:
```bash
python manage.py createsuperuser
```

Acesse: http://127.0.0.1:8000/admin
- Crie um usuário "cliente_teste"
- Vá para "Perfis de Cliente" e crie um perfil para ele

Opção B - Via Registro:
1. Acesse http://127.0.0.1:8000/accounts/customer-register/
2. Preencha: email, username, password
3. Será auto-logado

### 3. Criar um Produto (Vendedor)

1. Acesse http://127.0.0.1:8000/accounts/seller-register/
2. Crie um vendedor "vendedor_teste"
3. Logado como vendedor, acesse http://127.0.0.1:8000/products/create/
4. Preencha o formulário:
   - Nome: "Placa Solar 100W"
   - Preço: 150.00
   - Quantidade: 10
   - Descrição: qualquer coisa
   - Imagem: upload ou URL

### 4. Simular Compra (Cliente)

1. Logado como cliente, acesse http://127.0.0.1:8000/products/
2. Clique em um produto → "Adicionar ao Carrinho"
3. Acesse http://127.0.0.1:8000/cart/
4. Clique em "Finalizar Compra"
5. Será redirecionado para `/orders/checkout/`

### 5. Teste de Pagamento com Stripe

Na página de checkout, você verá:
- Resumo do pedido
- Formulário de pagamento
- Campo do Stripe Card Element

**Use estes dados de teste:**

| Cenário | Número | Data | CVC |
|---------|--------|------|-----|
| ✅ Sucesso | 4242 4242 4242 4242 | 12/25 | 123 |
| ❌ Falha | 4000 0000 0000 0002 | 12/25 | 123 |
| 🔐 3D Secure | 4000 0025 0000 3155 | 12/25 | 123 |

**Nome**: qualquer nome
**Email**: qualquer email

### 6. Acompanhar Pagamento

Após clicar em "Processar Pagamento":

1. **Com sucesso:**
   - Será redirecionado para `/payments/success/{order_id}/`
   - Verá confirmação do pagamento
   - Poderá acessar "Meus Pedidos"

2. **Cancelado:**
   - Será redirecionado para `/payments/cancel/{order_id}/`
   - Voltará ao carrinho

## 🔍 Verificar Dados no Admin

1. Acesse http://127.0.0.1:8000/admin
2. Seção "Payments":
   - **Payments**: Veja status de cada pagamento
   - **Payment Logs**: Veja timeline de eventos

3. Seção "Orders":
   - **Orders**: Veja pedidos criados
   - **Order Items**: Veja produtos de cada pedido

## 🛠️ Debugging

### Ver Logs em Tempo Real

Abra o terminal onde rodou `runserver` para ver:
- Requisições HTTP
- Erros do Django
- Prints de debug

### Verificar Estoque

```bash
python manage.py shell
>>> from products.models import Product
>>> p = Product.objects.first()
>>> p.quantity  # Ver quantidade antes da compra
>>> # Após compra, rode novamente
>>> p.refresh_from_db()
>>> p.quantity  # Deve ter decrementado
```

### Verificar Pagamento

```bash
python manage.py shell
>>> from payments.models import Payment, PaymentLog
>>> p = Payment.objects.last()
>>> p.status  # pending, processing, succeeded, failed
>>> p.stripe_session_id
>>> p.logs.all()  # Ver eventos
>>> for log in p.logs.all():
...     print(f"{log.event_type}: {log.details}")
```

### Verificar Carrinho em Sessão

```bash
python manage.py shell
>>> from django.contrib.sessions.models import Session
>>> from django.contrib.sessions.backends.db import SessionStore
>>> # Encontre a sessão ativa
>>> s = Session.objects.last()
>>> s.get_decoded()  # Ver dados da sessão incluindo carrinho
```

## ⚠️ Problemas Comuns

### 1. "Stripe API key not found"

**Solução:**
- Verifique se `.env` existe na raiz do projeto
- Verifique se `STRIPE_PUBLIC_KEY` e `STRIPE_SECRET_KEY` estão definidos
- Reinicie o servidor: `Ctrl+C` e `python manage.py runserver`

### 2. "Apenas clientes podem fazer compras"

**Solução:**
- Você está logado como vendedor
- Crie/acesse uma conta de cliente: http://127.0.0.1:8000/accounts/customer-register/

### 3. "Cartão inválido" no Stripe

**Solução:**
- Use os cartões de teste acima
- Certifique-se de que data está no futuro (ex: 12/25)
- CVC deve ter 3 dígitos

### 4. "Carrinho vazio após pagamento"

**Solução:**
- Normal! O carrinho é limpo após criar a sessão de pagamento
- Os itens estarão no Order (pedido)

## 📊 Checklist Completo de Testes

- [ ] Criar usuário cliente
- [ ] Criar usuário vendedor  
- [ ] Criar produto como vendedor
- [ ] Adicionar produto ao carrinho como cliente
- [ ] Acessar página de checkout
- [ ] Pagar com cartão de teste (sucesso)
- [ ] Verificar Order criado no admin
- [ ] Verificar Payment criado no admin
- [ ] Verificar estoque foi decrementado
- [ ] Acessar "Meus Pedidos"
- [ ] Tentar pagar com cartão que falha
- [ ] Verificar Payment com status "failed"

## 🚀 Próximos Passos em Produção

1. Obter chaves de produção do Stripe (começam com `live_`)
2. Configurar webhook para receber eventos reais
3. Trocar `DEBUG = False` em `settings.py`
4. Usar banco de dados PostgreSQL
5. Configurar HTTPS/SSL (obrigatório para pagamentos)
6. Adicionar email de confirmação
7. Implementar sistema de reembolsos
