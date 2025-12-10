from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_payment_confirmation_email(order, payment=None):
    """
    Envia email de confirmação de pagamento para o cliente.
    
    Args:
        order: Instância de Order
        payment: Instância de Payment (opcional)
    
    Returns:
        bool: True se email foi enviado, False caso contrário
    """
    try:
        # Preparar contexto para o template
        context = {
            'order': order,
            'payment': payment,
            'customer_name': order.customer.user.get_full_name() or order.customer.user.username,
            'site_url': settings.SITE_URL,
        }

        # Renderizar templates de texto e HTML
        text_message = render_to_string('payments/email_payment_confirmation.txt', context)
        html_message = render_to_string('payments/email_payment_confirmation.html', context)

        # Criar e enviar email
        email = EmailMultiAlternatives(
            subject='Confirmação de Pagamento - Solar Store #' + str(order.id),
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.customer.user.email],
        )
        email.attach_alternative(html_message, "text/html")
        
        result = email.send()
        
        # Log de sucesso
        print(f'✅ Email de confirmação enviado para {order.customer.user.email}')
        return result > 0
        
    except Exception as e:
        # Log de erro
        print(f'❌ Erro ao enviar email de confirmação: {str(e)}')
        return False
