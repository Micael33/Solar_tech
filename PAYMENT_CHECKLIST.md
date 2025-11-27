# ✅ Checklist de Configuração - Sistema de Pagamento

## 📋 Pré-Requisitos

- [ ] Python 3.11+ instalado
- [ ] Django 5.2.8+ instalado
- [ ] Virtual environment criado e ativado
- [ ] Pacotes instalados: `pip install stripe python-dotenv`

## 🔑 Configuração Stripe

### Desenvolvimento (Teste)

- [ ] Acessar https://dashboard.stripe.com/apikeys
- [ ] Copiar **Publishable key** (começa com `pk_test_`)
- [ ] Copiar **Secret key** (começa com `sk_test_`)
- [ ] Criar arquivo `.env` na raiz do projeto
- [ ] Preencher `.env`:
  ```env
  STRIPE_PUBLIC_KEY=pk_test_seu_token_aqui
  STRIPE_SECRET_KEY=sk_test_seu_token_aqui
  STRIPE_WEBHOOK_SECRET=whsec_local_test_token
  SITE_URL=http://127.0.0.1:8000
  ```

### Produção (Live)

- [ ] Ativar modo Live em https://dashboard.stripe.com/settings/account
- [ ] Copiar **Live Publishable key** (começa com `pk_live_`)
- [ ] Copiar **Live Secret key** (começa com `sk_live_`)
- [ ] Atualizar `.env` com chaves live
- [ ] Atualizar `SITE_URL` com domínio real (HTTPS)
- [ ] Configurar webhook (ver seção abaixo)

## 🛠️ Instalação e Setup

### 1. Instalar Dependências

```bash
# Criar virtual environment
python -m venv venv

# Ativar virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar pacotes
pip install stripe python-dotenv
```

- [ ] Pacotes instalados com sucesso

### 2. Configurar Django

- [ ] Arquivo `.env` criado e preenchido
- [ ] `payments` app adicionado em `INSTALLED_APPS`
- [ ] `stripe.api_key` configurado em `settings.py`
- [ ] Variáveis `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` carregadas

### 3. Aplicar Migrações

```bash
python manage.py makemigrations payments
python manage.py migrate
```

- [ ] Migrações criadas
- [ ] Migrações aplicadas com sucesso

## 🧪 Testes Básicos

### 1. Verificar Configuração

```bash
python manage.py check
```

- [ ] Nenhum erro reportado

### 2. Criar Dados de Teste

```bash
python manage.py shell

# Dentro do shell:
from django.contrib.auth.models import User
from accounts.models import CustomerProfile

# Criar usuário cliente
user = User.objects.create_user(
    username='cliente_teste',
    email='cliente@test.com',
    password='senha123'
)

# Criar perfil de cliente
profile = CustomerProfile.objects.create(user=user)

# Criar vendedor
vendor = User.objects.create_user(
    username='vendedor_teste',
    email='vendedor@test.com',
    password='senha123'
)

from accounts.models import SellerProfile
seller = SellerProfile.objects.create(
    user=vendor,
    shop_name='Loja Teste'
)

exit()
```

- [ ] Usuários de teste criados

### 3. Criar Produto de Teste

```bash
python manage.py shell

from products.models import Product
from accounts.models import SellerProfile

seller = SellerProfile.objects.first()
product = Product.objects.create(
    seller=seller,
    name='Placa Solar 100W',
    slug='placa-solar-100w',
    price=150.00,
    quantity=10,
    description='Excelente produto de teste'
)

exit()
```

- [ ] Produto criado

### 4. Testar Fluxo de Pagamento

1. [ ] Iniciar servidor: `python manage.py runserver`
2. [ ] Acessar http://127.0.0.1:8000
3. [ ] Login como cliente
4. [ ] Adicionar produto ao carrinho
5. [ ] Ir para /cart/
6. [ ] Clicar "Finalizar Compra"
7. [ ] Ver página de checkout com Stripe Card Element

### 5. Testar Cartão de Teste

Na página de checkout:
- [ ] Inserir cartão: `4242 4242 4242 4242`
- [ ] Data: `12/25`
- [ ] CVC: `123`
- [ ] Nome: qualquer nome
- [ ] Clicar "Processar Pagamento"

Resultado esperado:
- [ ] Redireciona para página do Stripe Checkout
- [ ] Após "Pay", redireciona para /payments/success/
- [ ] Página mostra "Pagamento Confirmado"

### 6. Verificar Dados no Admin

1. [ ] Acessar http://127.0.0.1:8000/admin
2. [ ] Login como admin
3. [ ] Ir para "Payments" → "Payments"
4. [ ] Ver novo Payment com status "succeeded"
5. [ ] Ir para "Orders" → "Orders"
6. [ ] Ver novo Order com `paid=True`
7. [ ] Verificar que estoque foi decrementado

## 🔐 Segurança

### Código

- [ ] `.env` adicionado ao `.gitignore`
- [ ] Nenhuma chave exposta em arquivo Python
- [ ] CSRF token presente em formulário de checkout
- [ ] Validação de autenticação em todas as views
- [ ] Permissões verificadas (cliente vs vendedor)

### Comunicação

- [ ] HTTPS obrigatório em produção (alterar `SITE_URL`)
- [ ] Webhook configurado com HTTPS
- [ ] Assinatura de webhook verificada com `STRIPE_WEBHOOK_SECRET`

## 🪝 Webhook Configuration

### Teste Local (Desenvolvimento)

Opção 1: Usar Stripe CLI
```bash
# Baixar: https://stripe.com/docs/stripe-cli
stripe listen --forward-to http://127.0.0.1:8000/payments/webhook/

# Copiar evento de teste
stripe trigger payment_intent.succeeded
```

- [ ] Stripe CLI instalado e rodando
- [ ] Webhook testado com sucesso

### Produção

1. [ ] Acessar https://dashboard.stripe.com/webhooks
2. [ ] Clicar "Add endpoint"
3. [ ] Preencher URL: `https://seu-dominio.com/payments/webhook/`
4. [ ] Selecionar eventos:
   - [ ] `checkout.session.completed`
   - [ ] `charge.failed`
   - [ ] `payment_intent.succeeded`
5. [ ] Criar endpoint
6. [ ] Copiar "Signing secret"
7. [ ] Atualizar `.env`: `STRIPE_WEBHOOK_SECRET=whsec_...`

## 📊 Teste Completo (Checklist Final)

**Fluxo 1: Pagamento Bem-Sucedido**
- [ ] Login como cliente
- [ ] Adicionar produto ao carrinho
- [ ] Ir a checkout
- [ ] Usar cartão `4242 4242 4242 4242`
- [ ] Confirmação de sucesso
- [ ] Order criado em admin
- [ ] Payment com status `succeeded`
- [ ] Estoque decrementado

**Fluxo 2: Pagamento Falhado**
- [ ] Login como cliente
- [ ] Adicionar produto ao carrinho
- [ ] Ir a checkout
- [ ] Usar cartão `4000 0000 0000 0002`
- [ ] Ver mensagem de erro
- [ ] Payment com status `failed`
- [ ] Estoque não foi alterado

**Fluxo 3: Pagamento Cancelado**
- [ ] Login como cliente
- [ ] Adicionar produto ao carrinho
- [ ] Ir a checkout
- [ ] Clicar em "Cancel" na página Stripe
- [ ] Redirecionar para `/payments/cancel/`
- [ ] Payment com status `canceled`
- [ ] Voltar ao carrinho

**Fluxo 4: Admin e Auditoria**
- [ ] Acessar admin de Payments
- [ ] Visualizar Payment
- [ ] Expandir "Dados do Stripe"
- [ ] Ver resposta JSON do Stripe
- [ ] Ver PaymentLog com timeline
- [ ] Filtrar por status
- [ ] Filtrar por data

## 🚀 Produção - Checklist Adicional

- [ ] `DEBUG = False` em settings.py
- [ ] `ALLOWED_HOSTS` configurado com domínio real
- [ ] HTTPS ativado (SSL/TLS)
- [ ] Usar banco PostgreSQL
- [ ] Configurar backups automáticos
- [ ] Email de confirmação funcionando
- [ ] STRIPE_WEBHOOK_SECRET atualizado para token de produção
- [ ] Testado pagamento real com pequeno valor
- [ ] Reembolso testado (se implementado)
- [ ] Monitorar Stripe Dashboard para erros

## 📞 Troubleshooting

### Erro: "Stripe API key not found"
- [ ] Verificar se `.env` existe
- [ ] Verificar se `STRIPE_PUBLIC_KEY` e `STRIPE_SECRET_KEY` estão definidos
- [ ] Reiniciar servidor Django

### Erro: "Invalid Signing Secret"
- [ ] Copiar `Signing Secret` correto do Stripe
- [ ] Atualizar `STRIPE_WEBHOOK_SECRET`
- [ ] Reiniciar servidor

### Erro: "CSRF token missing or incorrect"
- [ ] Verificar se formulário tem `{% csrf_token %}`
- [ ] Limpar cookies do navegador
- [ ] Testar em novo navegador/incógnito

### Cartão Aceito mas não aparece confirmação
- [ ] Verificar logs do servidor Django
- [ ] Verificar se webhook foi recebido (Stripe Dashboard → Events)
- [ ] Ir diretamente para `/payments/success/{order_id}/`

### Estoque não decrementou
- [ ] Verificar se Payment tem status `succeeded`
- [ ] Verificar se webhook foi processado (PaymentLog)
- [ ] Verificar logs de erro no Django

## 📚 Próximas Leituras

- [ ] `STRIPE_SETUP.md` - Guia detalhado
- [ ] `PAYMENT_TESTING.md` - Testes práticos
- [ ] `PAYMENT_API_EXAMPLES.md` - Exemplos de código
- [ ] `PAYMENT_IMPLEMENTATION.md` - Resumo técnico

## ✨ Status Final

- [ ] Todas as etapas completadas
- [ ] Payments funcionando em desenvolvimento
- [ ] Documentação revogida
- [ ] Pronto para produção

---

**Data de Conclusão**: _______________
**Testado por**: _______________
**Aprovado em Produção**: _______________
