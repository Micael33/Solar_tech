# Exemplos de Uso - API de Pagamento

## 🐚 Shell Django - Exemplos Práticos

### 1. Listar Pagamentos Recentes

```python
from payments.models import Payment
from django.utils import timezone
from datetime import timedelta

# Últimas 24 horas
recent = Payment.objects.filter(
    created_at__gte=timezone.now() - timedelta(days=1)
).order_by('-created_at')

for p in recent:
    print(f"Order {p.order.id}: R$ {p.amount} - Status: {p.get_status_display()}")
```

### 2. Verificar Pagamentos por Status

```python
from payments.models import Payment

# Pagamentos bem-sucedidos
succeeded = Payment.objects.filter(status='succeeded')
print(f"Total pago: R$ {sum(p.amount for p in succeeded)}")

# Pagamentos pendentes
pending = Payment.objects.filter(status='pending')
for p in pending:
    print(f"Pendente: Order {p.order.id} - {p.customer_name}")

# Pagamentos falhados
failed = Payment.objects.filter(status='failed')
for p in failed:
    print(f"Falhou: Order {p.order.id} - Motivo: {p.stripe_response}")
```

### 3. Rastrear Timeline de Pagamento

```python
from payments.models import Payment

payment = Payment.objects.get(id=1)
print(f"\n--- Timeline do Pagamento {payment.id} ---")
for log in payment.logs.all():
    print(f"[{log.created_at.strftime('%H:%M:%S')}] {log.event_type}")
    if log.details:
        for k, v in log.details.items():
            print(f"  - {k}: {v}")
```

### 4. Recuperar Dados de Webhook

```python
from payments.models import Payment

payment = Payment.objects.last()
if payment.stripe_response:
    print("Resposta do Stripe:")
    import json
    print(json.dumps(payment.stripe_response, indent=2))
```

### 5. Verificar Estoque Após Pagamento

```python
from orders.models import Order
from products.models import Product

order = Order.objects.get(id=1)
print(f"\n--- Produtos do Pedido {order.id} ---")
for item in order.items.all():
    product = item.product
    print(f"{item.quantity}x {product.name}")
    print(f"  Estoque atual: {product.quantity}")
```

### 6. Calcular Estatísticas de Pagamento

```python
from payments.models import Payment
from django.db.models import Sum, Count
from datetime import datetime

# Faturamento total
total_revenue = Payment.objects.filter(
    status='succeeded'
).aggregate(Sum('amount'))['amount__sum'] or 0

# Ticket médio
avg_order = Payment.objects.filter(
    status='succeeded'
).aggregate(Sum('amount') / Count('id'))

# Últimos 7 dias
from datetime import timedelta
from django.utils import timezone

week_ago = timezone.now() - timedelta(days=7)
week_revenue = Payment.objects.filter(
    status='succeeded',
    paid_at__gte=week_ago
).aggregate(Sum('amount'))['amount__sum'] or 0

print(f"Faturamento total: R$ {total_revenue:.2f}")
print(f"Faturamento (7 dias): R$ {week_revenue:.2f}")
print(f"Número de pedidos: {Payment.objects.filter(status='succeeded').count()}")
print(f"Taxa de sucesso: {Payment.objects.filter(status='succeeded').count() / Payment.objects.count() * 100:.1f}%")
```

### 7. Reprocessar Webhook Manualmente

```python
from payments.views import handle_checkout_session_completed
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Se precisar reprocessar um webhook específico
session = stripe.checkout.Session.retrieve('cs_test_...')
handle_checkout_session_completed(session)
print("Webhook reprocessado manualmente")
```

## 📝 Exemplos Python Avançados

### 8. Criar Refund (Reembolso) - Futura Implementação

```python
import stripe
from django.conf import settings
from payments.models import Payment, PaymentLog

stripe.api_key = settings.STRIPE_SECRET_KEY

def refund_payment(payment_id, reason="Solicitado pelo cliente"):
    payment = Payment.objects.get(id=payment_id)
    
    if payment.status != 'succeeded':
        print("Só pode reembolsar pagamentos bem-sucedidos")
        return False
    
    try:
        refund = stripe.Refund.create(
            payment_intent=payment.stripe_payment_intent_id,
            reason=reason
        )
        
        # Log do reembolso
        PaymentLog.objects.create(
            payment=payment,
            event_type='refund_initiated',
            details={'refund_id': refund.id}
        )
        
        print(f"Reembolso iniciado: {refund.id}")
        return True
    except Exception as e:
        print(f"Erro ao reembolsar: {str(e)}")
        return False

# Usar:
# refund_payment(1, reason="Cliente solicitou cancelamento")
```

### 9. Listar Histórico de Alterações de Payment

```python
from payments.models import PaymentLog

def payment_history(payment_id):
    logs = PaymentLog.objects.filter(
        payment_id=payment_id
    ).order_by('created_at')
    
    print(f"\n--- Histórico do Pagamento {payment_id} ---")
    for log in logs:
        print(f"\n{log.created_at.isoformat()}")
        print(f"Evento: {log.get_event_type_display()}")
        print(f"Detalhes: {log.details}")

# Usar:
# payment_history(1)
```

### 10. Exportar Pagamentos para CSV

```python
import csv
from payments.models import Payment

def export_payments_csv(filename='payments.csv'):
    payments = Payment.objects.filter(
        status='succeeded'
    ).select_related('order', 'order__customer')
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'ID Pagamento', 'ID Pedido', 'Cliente', 'Email',
            'Valor', 'Data', 'Método', 'Status'
        ])
        
        for p in payments:
            writer.writerow([
                p.id,
                p.order.id,
                p.customer_name,
                p.customer_email,
                f"R$ {p.amount:.2f}",
                p.paid_at.strftime('%d/%m/%Y %H:%M'),
                p.get_payment_method_display(),
                p.get_status_display(),
            ])
    
    print(f"Exportado: {filename}")

# Usar:
# export_payments_csv('/path/to/payments.csv')
```

## 🔧 Consultas SQL Úteis (para debug avançado)

### Pagamentos com maior valor

```sql
SELECT * FROM payments_payment 
ORDER BY amount DESC 
LIMIT 10;
```

### Timeline de pagamentos hoje

```sql
SELECT p.id, p.status, p.amount, p.created_at, pl.event_type
FROM payments_payment p
LEFT JOIN payments_paymentlog pl ON p.id = pl.payment_id
WHERE DATE(p.created_at) = DATE('now')
ORDER BY p.created_at DESC;
```

### Taxa de sucesso por método de pagamento

```sql
SELECT 
    payment_method,
    COUNT(*) as total,
    SUM(CASE WHEN status = 'succeeded' THEN 1 ELSE 0 END) as sucesso,
    ROUND(100.0 * SUM(CASE WHEN status = 'succeeded' THEN 1 ELSE 0 END) / COUNT(*), 2) as taxa_sucesso
FROM payments_payment
GROUP BY payment_method;
```

## 🐛 Debugging Comum

### Problema: Pagamento fica em "pending"

```python
from payments.models import Payment

p = Payment.objects.get(id=1)
print(f"Status: {p.status}")
print(f"Stripe Session: {p.stripe_session_id}")
print(f"Logs: {[log.event_type for log in p.logs.all()]}")

# Se não tem 'payment_confirmed' ou 'webhook_checkout_completed',
# o webhook não foi recebido
```

### Problema: Estoque não foi decrementado

```python
from orders.models import Order

order = Order.objects.get(id=1)
print(f"Paid: {order.paid}")
print(f"Payment exists: {hasattr(order, 'payment')}")

if hasattr(order, 'payment'):
    print(f"Payment status: {order.payment.status}")
    
# Se status é 'succeeded' mas estoque não mudou,
# verifique os logs de erro
```

## 🚀 Automação de Tarefas

### Encontrar pagamentos que precisam de ação

```python
from payments.models import Payment
from datetime import timedelta
from django.utils import timezone

# Pagamentos que falharam hoje
failed_today = Payment.objects.filter(
    status='failed',
    created_at__date=timezone.now().date()
)

print(f"Pagamentos falhados hoje: {failed_today.count()}")
for p in failed_today:
    print(f"  - {p.customer_name}: {p.order.id}")

# Pagamentos antigos pendentes (possível webhook perdido)
old_pending = Payment.objects.filter(
    status='pending',
    created_at__lt=timezone.now() - timedelta(hours=1)
)

print(f"Pagamentos antigos pendentes: {old_pending.count()}")
# Considerar enviar email de follow-up
```

## 📈 Dashboard de Métricas

```python
from payments.models import Payment
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

def payment_dashboard():
    now = timezone.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    metrics = {
        'hoje': {
            'total': Payment.objects.filter(created_at__gte=today).count(),
            'sucesso': Payment.objects.filter(status='succeeded', created_at__gte=today).count(),
            'faturamento': Payment.objects.filter(status='succeeded', created_at__gte=today).aggregate(Sum('amount'))['amount__sum'] or 0,
        },
        'semana': {
            'total': Payment.objects.filter(created_at__gte=week_ago).count(),
            'sucesso': Payment.objects.filter(status='succeeded', created_at__gte=week_ago).count(),
            'faturamento': Payment.objects.filter(status='succeeded', created_at__gte=week_ago).aggregate(Sum('amount'))['amount__sum'] or 0,
        },
        'mês': {
            'total': Payment.objects.filter(created_at__gte=month_ago).count(),
            'sucesso': Payment.objects.filter(status='succeeded', created_at__gte=month_ago).count(),
            'faturamento': Payment.objects.filter(status='succeeded', created_at__gte=month_ago).aggregate(Sum('amount'))['amount__sum'] or 0,
        },
    }
    
    for period, data in metrics.items():
        print(f"\n📊 {period.upper()}")
        print(f"  Total: {data['total']} transações")
        print(f"  Sucesso: {data['sucesso']} ({100*data['sucesso']/max(1, data['total']):.0f}%)")
        print(f"  Faturamento: R$ {data['faturamento']:.2f}")

payment_dashboard()
```

## ⚙️ Variáveis de Ambiente Úteis

```bash
# Para logging detalhado do Stripe
export STRIPE_LOG_LEVEL=DEBUG

# Para modo teste (sem enviar para API Stripe)
export STRIPE_TEST_MODE=true

# Para debug de webhook
export WEBHOOK_DEBUG=true
```

---

**Dica**: Use `python manage.py shell` para acessar esses exemplos interativamente!
