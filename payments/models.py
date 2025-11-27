from django.db import models
from django.contrib.auth.models import User
from orders.models import Order


class Payment(models.Model):
    """Modelo para armazenar informações de pagamento"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('succeeded', 'Sucesso'),
        ('failed', 'Falhou'),
        ('canceled', 'Cancelado'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Cartão de Crédito'),
        ('pix', 'Pix'),
        ('boleto', 'Boleto'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    stripe_session_id = models.CharField(max_length=255, unique=True, db_index=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Valor em reais
    currency = models.CharField(max_length=3, default='BRL')
    
    # Dados do pagador
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=255)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Resposta do Stripe
    stripe_response = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f'Payment {self.id} - Order {self.order.id} - {self.status}'
    
    class Meta:
        ordering = ['-created_at']


class PaymentLog(models.Model):
    """Log de eventos de pagamento para auditoria"""
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='logs')
    event_type = models.CharField(max_length=50)  # e.g., 'session_created', 'payment_succeeded', 'webhook_received'
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Log {self.id} - {self.event_type} - Payment {self.payment.id}'
    
    class Meta:
        ordering = ['-created_at']
