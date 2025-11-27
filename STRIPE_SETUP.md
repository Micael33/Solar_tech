# Sistema de Pagamento com Stripe

Este projeto integra o **Stripe** como processador de pagamentos para o e-commerce Solar Store.

## 📋 Requisitos

- Python 3.11+
- Django 5.2+
- `stripe` SDK
- `python-dotenv`

## 🚀 Configuração Inicial

### 1. Instalar Dependências

```bash
pip install stripe python-dotenv
```

### 2. Obter Chaves do Stripe

1. Acesse [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
2. Copie suas chaves de teste (começam com `pk_test_` e `sk_test_`)
3. Guarde-as com segurança

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Stripe Keys (Test)
STRIPE_PUBLIC_KEY=pk_test_seu_token_aqui
STRIPE_SECRET_KEY=sk_test_seu_token_aqui
STRIPE_WEBHOOK_SECRET=whsec_seu_token_aqui

# Site URL (para redirects após pagamento)
SITE_URL=http://127.0.0.1:8000
```

**Produção:**
- Substitua as chaves de teste (`pk_test_` e `sk_test_`) por chaves de produção (`pk_live_` e `sk_live_`)
- Atualize `SITE_URL` para seu domínio real

### 4. Aplicar Migrações

```bash
python manage.py migrate payments
```

## 🔧 Como Funciona o Fluxo de Pagamento

### 1. **Adicionar ao Carrinho**
   - Cliente adiciona produtos ao carrinho
   - Carrinho é armazenado em sessão

### 2. **Checkout**
   - Cliente clica em "Finalizar Compra"
   - É redirecionado para `/orders/checkout/`
   - Visualiza resumo do pedido e formulário de pagamento

### 3. **Criar Sessão de Pagamento**
   - JavaScript do Stripe cria uma sessão via `POST /payments/create-session/`
   - A view valida o carrinho e cria um `Order` no banco
   - Stripe retorna `sessionId` e URL de redirecionamento

### 4. **Redirecionamento para Stripe Checkout**
   - Cliente é redirecionado para a página de checkout do Stripe
   - Insere dados do cartão de crédito

### 5. **Confirmação de Pagamento**
   - Stripe processa o pagamento
   - Se sucesso: redireciona para `/payments/success/{order_id}/`
   - Se cancelado: redireciona para `/payments/cancel/{order_id}/`

### 6. **Webhook (Confirmação Segura)**
   - Stripe envia webhook para `/payments/webhook/`
   - Verifica assinatura e atualiza status do `Payment`
   - Marca `Order` como pago
   - Decrementa estoque dos produtos

## 📊 Modelos de Dados

### `Payment`
Armazena informações de pagamento para cada pedido:
- `order` - Relacionamento OneToOne com Order
- `stripe_session_id` - ID da sessão Stripe
- `stripe_payment_intent_id` - ID do Payment Intent
- `status` - pending, processing, succeeded, failed, canceled
- `payment_method` - card, pix, boleto
- `amount` - Valor total
- `customer_email` e `customer_name`
- `paid_at` - Timestamp de confirmação

### `PaymentLog`
Log de auditoria de eventos de pagamento:
- `payment` - FK para Payment
- `event_type` - session_created, payment_succeeded, webhook_received, etc.
- `details` - JSON com dados do evento
- `created_at` - Timestamp

## 🧪 Teste com Cartões de Teste

Use os seguintes dados de teste com Stripe:

**Pagamento Bem-Sucedido:**
- Número: `4242 4242 4242 4242`
- Data: `12/25` (qualquer data futura)
- CVC: `123`

**Pagamento Falhará:**
- Número: `4000 0000 0000 0002`
- Data: `12/25`
- CVC: `123`

**3D Secure Requerido:**
- Número: `4000 0025 0000 3155`
- Data: `12/25`
- CVC: `123`

## 🔐 Webhook Configuration (Produção)

1. Acesse [Stripe Webhook Endpoints](https://dashboard.stripe.com/webhooks)
2. Adicione novo endpoint:
   - URL: `https://seu-dominio.com/payments/webhook/`
   - Eventos: 
     - `checkout.session.completed`
     - `charge.failed`
     - `payment_intent.succeeded`

3. Copie o `Signing Secret` (começa com `whsec_`)
4. Configure no `.env`: `STRIPE_WEBHOOK_SECRET=whsec_...`

## 🚨 Tratamento de Erros

A aplicação trata os seguintes cenários:

- **Estoque insuficiente**: Retorna erro antes de criar sessão
- **Carrinho vazio**: Redireciona para o carrinho
- **Pagamento falhou**: Redireciona para página de cancelamento
- **Webhook inválido**: Retorna 400 sem atualizar dados

## 📱 Futuras Melhorias

- [ ] Integração com Pix
- [ ] Integração com Boleto
- [ ] Envio de email de confirmação
- [ ] Sistema de reembolsos
- [ ] Parcelamento com Stripe
- [ ] Apple Pay e Google Pay
- [ ] Suporte a múltiplas moedas

## 🔗 Referências

- [Documentação Stripe](https://stripe.com/docs)
- [Stripe Python SDK](https://github.com/stripe/stripe-python)
- [Stripe Checkout](https://stripe.com/docs/payments/checkout)
- [Webhook Signing](https://stripe.com/docs/webhooks/signatures)

## 📞 Suporte

Para problemas ou dúvidas sobre integração:
- Verifique os logs em `Payment` e `PaymentLog` no admin
- Consulte a seção de eventos no [Stripe Dashboard](https://dashboard.stripe.com)
- Confirme que STRIPE_SECRET_KEY está corretamente configurado
