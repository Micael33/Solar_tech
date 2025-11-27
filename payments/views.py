import os
import json
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone
from django.conf import settings

from orders.models import Order
from accounts.models import CustomerProfile
from products.models import Product
from cart.views import _get_cart, _save_cart
from .models import Payment, PaymentLog

# Configurar chave do Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_payment_session(request):
    """Criar uma sessão de pagamento do Stripe Checkout"""
    try:
        customer_profile = getattr(request.user, 'customer_profile', None)
        if not customer_profile:
            return JsonResponse({'error': 'Apenas clientes podem fazer pagamentos'}, status=403)

        cart = _get_cart(request)
        if not cart:
            return JsonResponse({'error': 'Carrinho vazio'}, status=400)

        # Calcular total e validar estoque
        items = []
        total = 0
        for pid, qty in cart.items():
            try:
                product = Product.objects.get(id=pid)
            except Product.DoesNotExist:
                continue
            
            if product.quantity is not None and qty > product.quantity:
                return JsonResponse(
                    {'error': f'Estoque insuficiente para {product.name}'},
                    status=400
                )
            
            subtotal = product.price * qty
            items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })
            total += subtotal

        if not items:
            return JsonResponse({'error': 'Carrinho vazio'}, status=400)

        # Criar pedido no banco de dados
        with transaction.atomic():
            order = Order.objects.create(
                customer=customer_profile,
                total=total,
                paid=False  # Ainda não pago
            )
            
            # Criar items do pedido
            from orders.models import OrderItem
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )

            # Preparar items para o Stripe Checkout
            line_items = []
            for item in items:
                line_items.append({
                    'price_data': {
                        'currency': 'brl',
                        'unit_amount': int(item['product'].price * 100),  # Stripe usa centavos
                        'product_data': {
                            'name': item['product'].name,
                            'description': item['product'].description[:500] if item['product'].description else '',
                            'images': [settings.SITE_URL + item['product'].image.url] if item['product'].image else [],
                        },
                    },
                    'quantity': item['quantity'],
                })

            # Criar sessão de checkout no Stripe
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                customer_email=request.user.email,
                success_url=settings.SITE_URL + f'/payments/success/{order.id}/',
                cancel_url=settings.SITE_URL + f'/payments/cancel/{order.id}/',
                metadata={
                    'order_id': order.id,
                    'user_id': request.user.id,
                }
            )

            # Salvar informações de pagamento
            payment = Payment.objects.create(
                order=order,
                stripe_session_id=session.id,
                stripe_payment_intent_id=session.payment_intent,
                status='pending',
                amount=total,
                currency='BRL',
                customer_email=request.user.email,
                customer_name=request.user.get_full_name() or request.user.username,
            )

            # Log do evento
            PaymentLog.objects.create(
                payment=payment,
                event_type='session_created',
                details={
                    'session_id': session.id,
                    'url': session.url,
                }
            )

            # Limpar carrinho
            _save_cart(request, {})

            return JsonResponse({
                'sessionId': session.id,
                'redirectUrl': session.url,
            })

    except stripe.error.StripeError as e:
        return JsonResponse({'error': f'Erro do Stripe: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Erro ao criar sessão de pagamento: {str(e)}'}, status=500)


@login_required
def payment_success(request, order_id):
    """Página de sucesso após pagamento confirmado"""
    order = get_object_or_404(Order, id=order_id)
    
    # Verificar se o usuário é o dono do pedido
    if order.customer.user != request.user:
        messages.error(request, 'Acesso negado.')
        return redirect('home')
    
    # Buscar informações de pagamento
    payment = getattr(order, 'payment', None)
    
    # Se houver sessão do Stripe, recuperar status
    if payment and payment.stripe_session_id:
        try:
            session = stripe.checkout.Session.retrieve(payment.stripe_session_id)
            if session.payment_status == 'paid' and payment.status != 'succeeded':
                # Atualizar status de pagamento
                with transaction.atomic():
                    payment.status = 'succeeded'
                    payment.paid_at = timezone.now()
                    payment.stripe_response = session
                    payment.save()
                    
                    order.paid = True
                    order.save()
                    
                    PaymentLog.objects.create(
                        payment=payment,
                        event_type='payment_confirmed',
                        details={'session': session.id}
                    )
                    
                    # Decrementar estoque
                    for item in order.items.all():
                        if item.product and item.product.quantity is not None:
                            item.product.quantity = max(0, item.product.quantity - item.quantity)
                            item.product.save()
        except stripe.error.StripeError as e:
            messages.warning(request, 'Não foi possível verificar o status do pagamento. Entre em contato com o suporte.')
    
    return render(request, 'orders/payment_success.html', {'order': order, 'payment': payment})


@login_required
def payment_cancel(request, order_id):
    """Página de cancelamento de pagamento"""
    order = get_object_or_404(Order, id=order_id)
    
    # Verificar se o usuário é o dono do pedido
    if order.customer.user != request.user:
        messages.error(request, 'Acesso negado.')
        return redirect('home')
    
    # Atualizar status de pagamento
    payment = getattr(order, 'payment', None)
    if payment:
        payment.status = 'canceled'
        payment.save()
        
        PaymentLog.objects.create(
            payment=payment,
            event_type='payment_canceled',
            details={}
        )
    
    messages.warning(request, 'Seu pagamento foi cancelado. A compra não foi finalizada.')
    return redirect('cart_detail')


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Webhook para receber eventos do Stripe"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': 'Payload inválido'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Assinatura inválida'}, status=400)

    # Processar eventos
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session_completed(session)
    
    elif event['type'] == 'charge.failed':
        charge = event['data']['object']
        handle_charge_failed(charge)
    
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_intent_succeeded(payment_intent)

    return JsonResponse({'status': 'success'})


def handle_checkout_session_completed(session):
    """Tratar conclusão da sessão de checkout"""
    order_id = session.get('metadata', {}).get('order_id')
    if not order_id:
        return
    
    try:
        order = Order.objects.get(id=order_id)
        payment = getattr(order, 'payment', None)
        
        if payment:
            payment.status = 'succeeded'
            payment.paid_at = timezone.now()
            payment.stripe_response = session
            payment.save()
            
            order.paid = True
            order.save()
            
            PaymentLog.objects.create(
                payment=payment,
                event_type='webhook_checkout_completed',
                details={'session_id': session.id}
            )
            
            # Decrementar estoque
            for item in order.items.all():
                if item.product and item.product.quantity is not None:
                    item.product.quantity = max(0, item.product.quantity - item.quantity)
                    item.product.save()
    except Order.DoesNotExist:
        pass


def handle_charge_failed(charge):
    """Tratar falha de cobrança"""
    try:
        payment_intent_id = charge.get('payment_intent')
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
        
        payment.status = 'failed'
        payment.save()
        
        PaymentLog.objects.create(
            payment=payment,
            event_type='webhook_charge_failed',
            details={
                'charge_id': charge.get('id'),
                'failure_message': charge.get('failure_message'),
            }
        )
    except Payment.DoesNotExist:
        pass


def handle_payment_intent_succeeded(payment_intent):
    """Tratar sucesso de payment intent"""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
        
        if payment.status != 'succeeded':
            payment.status = 'succeeded'
            payment.paid_at = timezone.now()
            payment.save()
            
            PaymentLog.objects.create(
                payment=payment,
                event_type='webhook_payment_intent_succeeded',
                details={'payment_intent_id': payment_intent['id']}
            )
    except Payment.DoesNotExist:
        pass
