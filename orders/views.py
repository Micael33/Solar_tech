from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from cart.views import _get_cart
from .models import Order, OrderItem
from accounts.models import CustomerProfile
from products.models import Product


@login_required
def checkout(request):
	"""Exibir página de checkout com opções de pagamento"""
	# only customers can checkout
	customer_profile = getattr(request.user, 'customer_profile', None)
	if not customer_profile:
		messages.error(request, 'Apenas clientes podem finalizar compras.')
		return redirect('home')

	cart = _get_cart(request)
	if not cart:
		messages.error(request, 'Seu carrinho está vazio.')
		return redirect('cart_detail')

	items = []
	total = 0
	for pid, qty in cart.items():
		try:
			product = Product.objects.get(id=pid)
		except Product.DoesNotExist:
			continue
		subtotal = product.price * qty
		items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
		total += subtotal
		# Validate stock
		if product.quantity is not None and qty > product.quantity:
			messages.error(request, f'Estoque insuficiente para {product.name}.')
			return redirect('cart_detail')

	context = {
		'items': items,
		'total': total,
		'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
	}
	return render(request, 'orders/checkout.html', context)


@login_required
def order_success(request, order_id):
	"""Página de sucesso após pagamento confirmado (gerenciada pelo payments app)"""
	order = Order.objects.filter(id=order_id, customer__user=request.user).first()
	if not order:
		messages.error(request, 'Pedido não encontrado.')
		return redirect('home')
	
	payment = getattr(order, 'payment', None)
	context = {
		'order': order,
		'payment': payment,
	}
	return render(request, 'orders/order_success.html', context)


@login_required
def order_list(request):
	"""Listar pedidos do cliente"""
	# only customers can view their orders
	customer_profile = getattr(request.user, 'customer_profile', None)
	if not customer_profile:
		messages.error(request, 'Apenas clientes podem visualizar pedidos.')
		return redirect('home')
	orders = Order.objects.filter(customer=customer_profile).order_by('-created_at')
	return render(request, 'orders/order_list.html', {'orders': orders})
