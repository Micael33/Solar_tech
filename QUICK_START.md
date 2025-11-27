# 🚀 Quick Start - Sistema de Pagamento

## ⚡ 5 Minutos para Começar

### 1. Instalar (1 min)

```bash
cd c:\Users\micae\Solar_Tech
venv\Scripts\python.exe -m pip install stripe python-dotenv
```

### 2. Configurar (2 min)

```bash
# Editar .env na raiz do projeto
# Copiar de: https://dashboard.stripe.com/apikeys

STRIPE_PUBLIC_KEY=pk_test_seu_token_aqui
STRIPE_SECRET_KEY=sk_test_seu_token_aqui
STRIPE_WEBHOOK_SECRET=whsec_test
SITE_URL=http://127.0.0.1:8000
```

### 3. Executar (2 min)

```bash
python manage.py migrate
python manage.py runserver
```

## 🧪 Testar em 10 Passos

1. Abrir http://127.0.0.1:8000
2. Registrar como cliente: http://127.0.0.1:8000/accounts/customer-register/
3. Registrar como vendedor: http://127.0.0.1:8000/accounts/seller-register/
4. Fazer login como vendedor
5. Criar produto: http://127.0.0.1:8000/products/create/
6. Fazer logout e login como cliente
7. Adicionar produto ao carrinho
8. Ir para /orders/checkout/
9. Usar cartão: **4242 4242 4242 4242** (12/25 CVC: 123)
10. Confirmar sucesso!

## 💳 Cartões de Teste

| Cenário | Número | Data | CVC |
|---------|--------|------|-----|
| ✅ Sucesso | 4242 4242 4242 4242 | 12/25 | 123 |
| ❌ Falha | 4000 0000 0000 0002 | 12/25 | 123 |
| 🔐 3D Secure | 4000 0025 0000 3155 | 12/25 | 123 |

## 📂 Arquivos Importantes

| Arquivo | Função |
|---------|--------|
| `.env` | Chaves do Stripe |
| `payments/models.py` | Models Payment + PaymentLog |
| `payments/views.py` | Lógica de pagamento |
| `templates/orders/checkout.html` | Formulário Stripe |
| `STRIPE_SETUP.md` | Guia completo |
| `PAYMENT_TESTING.md` | Testes |
| `PAYMENT_CHECKLIST.md` | Checklist |

## 🔧 Comandos Úteis

```bash
# Criar superuser para admin
python manage.py createsuperuser

# Acessar admin
http://127.0.0.1:8000/admin

# Ver dados de pagamento
python manage.py shell
>>> from payments.models import Payment
>>> Payment.objects.all()

# Testar sem servidor
python manage.py check

# Limpar banco (⚠️ Cuidado!)
python manage.py flush
```

## 🐛 Erros Comuns

### "Stripe API key not found"
```
✅ Solução: Verificar .env e reiniciar servidor
```

### "Apenas clientes podem fazer pagamentos"
```
✅ Solução: Fazer login como cliente, não vendedor
```

### "Cartão inválido"
```
✅ Solução: Usar cartões de teste da tabela acima
```

### "Carrinho vazio"
```
✅ Solução: Adicionar produto antes de fazer checkout
```

## 📊 Verificar Status

### Admin Django
```
http://127.0.0.1:8000/admin/payments/payment/
```

### Shell Python
```bash
python manage.py shell

# Ver último pagamento
from payments.models import Payment
p = Payment.objects.last()
print(f"Status: {p.status}")  # pending, succeeded, failed
print(f"Valor: R$ {p.amount}")
print(f"Logs: {[log.event_type for log in p.logs.all()]}")
```

## 🔗 Links Úteis

| Link | Função |
|------|--------|
| https://dashboard.stripe.com/apikeys | Obter chaves |
| https://dashboard.stripe.com/webhooks | Configurar webhook |
| https://dashboard.stripe.com/events | Ver eventos |
| http://127.0.0.1:8000/admin | Admin local |
| http://127.0.0.1:8000/payments/docs | API docs (futura) |

## ✅ Checklist Rápido

- [ ] Pacotes instalados: `stripe`, `python-dotenv`
- [ ] `.env` criado com chaves Stripe
- [ ] Migrações aplicadas: `python manage.py migrate`
- [ ] Servidor rodando: `python manage.py runserver`
- [ ] Cliente criado
- [ ] Produto criado
- [ ] Checkout testado com cartão de teste
- [ ] Confirmação recebida
- [ ] Admin mostra Payment com status `succeeded`

## 🎓 Documentação Completa

```
├── STRIPE_SETUP.md           ← Leia isto primeiro!
├── PAYMENT_TESTING.md        ← Depois teste
├── PAYMENT_IMPLEMENTATION.md ← Entenda a arquitetura
├── PAYMENT_CHECKLIST.md      ← Para produção
├── PAYMENT_API_EXAMPLES.md   ← Exemplos de código
└── ARCHITECTURE.md           ← Diagramas
```

## 🚀 Deploying para Produção

```bash
# 1. Obter chaves live do Stripe
# Ir a: https://dashboard.stripe.com/settings/account

# 2. Atualizar .env com chaves live
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
SITE_URL=https://seu-dominio.com

# 3. Configurar webhook
# Ir a: https://dashboard.stripe.com/webhooks
# Adicionar: https://seu-dominio.com/payments/webhook/

# 4. Atualizar settings.py
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']

# 5. Usar servidor WSGI/GUNICORN
# Não usar django runserver!

# 6. Configurar HTTPS/SSL
# Usar Let's Encrypt ou similar
```

## 📞 Suporte

**Para problemas:**
1. Verificar logs: `python manage.py runserver`
2. Ver erro no admin: `/admin/payments/payment/`
3. Consultar Stripe Dashboard: https://dashboard.stripe.com/events
4. Ler documentação: `STRIPE_SETUP.md`

**Principais causas de erro:**
- Chave Stripe inválida/vencida
- `.env` não carregado
- Cartão de teste inválido
- Estoque insuficiente
- Usuário não é cliente

---

**Tempo para setup completo**: ~15 minutos
**Tempo para primeiro pagamento**: ~5 minutos
**Satisfação ao ver funcionando**: ∞
