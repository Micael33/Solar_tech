# 🏗️ Arquitetura do Sistema de Pagamento

## 📊 Diagrama de Fluxo

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENTE (NAVEGADOR)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Adiciona produto ao carrinho (sessão Django)                │
│  2. Clica "Finalizar Compra"                                    │
│  3. Vê página /orders/checkout/ com:                            │
│     - Resumo do pedido                                          │
│     - Formulário com Stripe Card Element                        │
│  4. Insere dados do cartão (não vão para nosso servidor!)       │
│  5. Clica "Processar Pagamento"                                 │
│  6. JavaScript faz POST para /payments/create-session/          │
│                                                                 │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│              NOSSO SERVIDOR (Django)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  A. View: create_payment_session()                              │
│     - Valida carrinho                                           │
│     - Valida estoque                                            │
│     - Cria Order (paid=False)                                   │
│     - Cria Payment (status=pending)                             │
│     - Log: session_created                                      │
│                                                                 │
│  B. Cria sessão no Stripe via API                               │
│     - Envia line_items com produtos                             │
│     - Envia success_url e cancel_url                            │
│     - Recebe sessionId do Stripe                                │
│                                                                 │
│  C. Retorna JSON com sessionId                                  │
│                                                                 │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                STRIPE (Serviço de Pagamento)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  7. Redireciona cliente para Stripe Checkout                    │
│  8. Cliente insere dados do cartão (seguro)                     │
│  9. Stripe processa pagamento com adquirente                    │
│  10. Pagamento aprovado ✅ ou recusado ❌                        │
│                                                                 │
└──────────────────┬──────────────────────────────────────────────┘
                   │
          ┌────────┴────────┐
          │                 │
          ▼ SUCESSO         ▼ ERRO
       ┌────┐          ┌────────┐
       │    │          │        │
       └────┘          └────────┘
          │                 │
          ▼                 ▼
    Redireciona para   Redireciona para
    /payments/        /payments/
    success/{id}/     cancel/{id}/
          │                 │
          └────────┬────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│              WEBHOOK (Confirmação Segura)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Stripe envia evento: checkout.session.completed                │
│  Nosso servidor valida assinatura                               │
│  Se válido:                                                     │
│    - Atualiza Payment (status=succeeded)                        │
│    - Marca Order (paid=True)                                    │
│    - Decrementa estoque dos produtos                            │
│    - Log: webhook_checkout_completed                            │
│                                                                 │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENTE (Confirmação)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Vê página de sucesso com:                                      │
│  - Confirmação do pagamento ✅                                   │
│  - Número do pedido                                             │
│  - Total pago                                                   │
│  - Instruções de rastreamento                                   │
│  - Link para "Meus Pedidos"                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🗄️ Estrutura de Banco de Dados

```
┌──────────────────────────────────┐
│        AUTH (Django Admin)       │
├──────────────────────────────────┤
│ User                             │
│ - id (PK)                        │
│ - username                       │
│ - email                          │
│ - password                       │
└────────┬────────────────┬────────┘
         │                │
         ▼                ▼
    ┌─────────┐    ┌──────────────┐
    │ Seller  │    │ Customer     │
    │ Profile │    │ Profile      │
    └────┬────┘    └──────┬───────┘
         │                │
         ▼                ▼
    ┌─────────────┐  ┌───────────┐
    │ Products    │  │ Orders    │
    │ - id (PK)   │  │ - id (PK) │
    │ - seller    │  │ - customer│
    │ - price     │  │ - total   │
    │ - quantity  │  │ - paid    │
    └──────┬──────┘  └─────┬─────┘
           │               │
           └───┬───────┬───┘
               │       │
               ▼       ▼
           ┌───────────────────┐
           │  OrderItem        │
           │  - id (PK)        │
           │  - order (FK)     │
           │  - product (FK)   │
           │  - quantity       │
           │  - price          │
           └─────────┬─────────┘
                     │
                     ▼
           ┌────────────────────┐
           │  Payment           │
           │  - id (PK)         │
           │  - order (OneToOne)│
           │  - status          │
           │  - amount          │
           │  - stripe_session  │
           │  - stripe_intent   │
           │  - paid_at         │
           └─────────┬──────────┘
                     │
                     ▼
           ┌────────────────────┐
           │  PaymentLog        │
           │  - id (PK)         │
           │  - payment (FK)    │
           │  - event_type      │
           │  - details (JSON)  │
           │  - created_at      │
           └────────────────────┘
```

## 🔄 Estados de Payment

```
ESTADOS POSSÍVEIS:

            ┌──────────────┐
            │   pending    │  ← Sessão criada, aguardando processamento
            │ (Padrão)     │
            └──────┬───────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
    ┌─────────┐         ┌──────────┐
    │processing│        │ canceled │
    │(Processando)│      │(Cancelado│
    └────┬────┘         └──────────┘
         │
    ┌────┴─────┐
    │           │
    ▼           ▼
┌───────────┐ ┌─────────┐
│succeeded  │ │ failed  │
│(Sucesso)  │ │(Falha)  │
└───────────┘ └─────────┘
   ✅ OK        ❌ Erro
```

## 🔑 Variáveis de Ambiente

```
.env (não commitir!)
├── STRIPE_PUBLIC_KEY        (pk_test_... ou pk_live_...)
├── STRIPE_SECRET_KEY        (sk_test_... ou sk_live_...)
├── STRIPE_WEBHOOK_SECRET    (whsec_...)
└── SITE_URL                 (http://localhost:8000 ou https://seu-dominio.com)

settings.py lê do .env e configura:
├── stripe.api_key = STRIPE_SECRET_KEY
├── STRIPE_PUBLIC_KEY (passado aos templates)
└── SITE_URL (para redirect URLs)
```

## 📁 Arquivos do Sistema de Pagamento

```
payments/                          (Nova app)
├── __init__.py
├── admin.py                        (Admin Django configurado)
├── apps.py
├── models.py                       (Payment + PaymentLog)
├── views.py                        (Todas as views de pagamento)
├── urls.py                         (Rotas /payments/*)
├── tests.py
├── migrations/
│   ├── 0001_initial.py            (Cria tabelas Payment + PaymentLog)
│   └── __pycache__/
├── templates/
│   └── payments/
│       └── payment_processing.html (Template de processamento)
└── __pycache__/

templates/orders/                   (Modificados)
├── checkout.html                   (Formulário Stripe integrado)
└── order_success.html              (Página de confirmação)

solar_store/
├── settings.py                     (Adicionado 'payments' app + config Stripe)
├── urls.py                         (Incluídas rotas /payments/)
└── .env                            (Novo arquivo com chaves)

Documentação criada:
├── STRIPE_SETUP.md                 (Guia de configuração)
├── PAYMENT_TESTING.md              (Guia de testes)
├── PAYMENT_IMPLEMENTATION.md       (Resumo técnico)
├── PAYMENT_API_EXAMPLES.md         (Exemplos de código)
└── PAYMENT_CHECKLIST.md            (Checklist de configuração)
```

## 🔐 Fluxo de Segurança

```
┌──────────────────────────────────────────────────────┐
│  CLIENTE NUNCA VÊ:                                   │
│  ❌ Stripe Secret Key                                │
│  ❌ Webhook Secret                                   │
│  ❌ Dados de pagamento raw (Stripe trata)            │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  SERVIDOR NUNCA VÊ:                                  │
│  ❌ Números inteiros de cartão                       │
│  ❌ Dados do cartão (Stripe trata)                   │
│  ✅ Apenas status de pagamento do Stripe             │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  SEGURANÇA IMPLEMENTADA:                             │
│  ✅ PCI DSS Compliant (Stripe Checkout)              │
│  ✅ CSRF Token em formulários                        │
│  ✅ Validação de assinatura de webhook               │
│  ✅ Autenticação de cliente                          │
│  ✅ Autorização de cliente (não vendedor)            │
│  ✅ Transações atômicas no BD                        │
│  ✅ Logs de auditoria de tudo                        │
└──────────────────────────────────────────────────────┘
```

## 🎯 Endpoints da API

```
POST /payments/create-session/
├── Autenticação: ✅ Requerida (Cliente)
├── Validação: Carrinho não vazio, estoque OK
├── Entrada: JSON (customer_name, customer_email)
├── Saída: JSON (sessionId, redirectUrl)
└── Efeitos: Cria Order + Payment no BD

GET/POST /payments/success/{order_id}/
├── Autenticação: ✅ Requerida (Dono do order)
├── Efeito: Verifica status Stripe, atualiza BD
└── Exibe: Página de confirmação

GET/POST /payments/cancel/{order_id}/
├── Autenticação: ✅ Requerida (Dono do order)
├── Efeito: Marca Payment como canceled
└── Redireciona: /cart/

POST /payments/webhook/
├── Autenticação: ❌ Não requerida
├── Validação: ✅ Assinatura Stripe verificada
├── Entrada: JSON do Stripe (webhook event)
├── Efeitos: Atualiza Payment + Order, decrementa estoque
└── Saída: JSON (status: success)
```

## 📈 Métricas Disponíveis

```
Admin Django (/admin/):

Payments:
├── Status: pending, processing, succeeded, failed, canceled
├── Método: card, pix, boleto
├── Filtros: por status, método, data
├── Busca: session_id, email, nome
├── Totalizações: Soma de amount por status

PaymentLog:
├── Timeline de eventos por pagamento
├── Tipos: session_created, payment_succeeded, webhook_received
├── Detalhes: JSON com informações do evento
└── Auditoria completa

Queries Python úteis:
├── Total faturado
├── Ticket médio
├── Taxa de sucesso
├── Pagamentos por período
└── Produtos mais vendidos
```

## 🚀 Roadmap Futuro

```
v1.0 (Atual)
├── ✅ Cartão de Crédito
├── ✅ Webhook de confirmação
├── ✅ Logs de auditoria
└── ✅ Admin Dashboard

v1.1 (Próximo)
├── 🔜 Integração Pix
├── 🔜 Parcelamento
├── 🔜 Email de confirmação
└── 🔜 Nota fiscal

v1.2
├── 🔜 Sistema de reembolsos
├── 🔜 Boleto bancário
├── 🔜 Apple Pay / Google Pay
└── 🔜 Suporte a múltiplas moedas

v2.0
├── 🔜 Assinatura/Recorrência
├── 🔜 Split de pagamento
├── 🔜 Dashboard de analytics
└── 🔜 API pública de integrações
```

---

**Status**: ✅ Completo e Pronto para Testes
**Última Atualização**: 27/11/2025
**Versão**: 1.0 (Produção-Ready)
