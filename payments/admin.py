from django.contrib import admin
from .models import Payment, PaymentLog


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status', 'amount', 'payment_method', 'created_at', 'paid_at')
    list_filter = ('status', 'payment_method', 'created_at', 'paid_at')
    search_fields = ('order__id', 'stripe_session_id', 'customer_email', 'customer_name')
    readonly_fields = ('stripe_session_id', 'stripe_payment_intent_id', 'created_at', 'updated_at', 'stripe_response')
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('order', 'customer_name', 'customer_email')
        }),
        ('Informações de Pagamento', {
            'fields': ('status', 'payment_method', 'amount', 'currency', 'paid_at')
        }),
        ('Dados do Stripe', {
            'fields': ('stripe_session_id', 'stripe_payment_intent_id', 'stripe_response'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'event_type', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('payment__id', 'event_type')
    readonly_fields = ('payment', 'event_type', 'details', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
