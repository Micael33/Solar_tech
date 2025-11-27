from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.views import _get_cart, _save_cart
from .models import Order, OrderItem
from accounts.models import CustomerProfile
from products.models import Product
from django.db import transaction


@login_required
def checkout(request):
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
	products_to_update = []
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
		products_to_update.append((product, qty))

	if request.method == 'POST':
		# Process payment simulation and create order atomically
		try:
			with transaction.atomic():
				order = Order.objects.create(customer=customer_profile, total=total, paid=True)
				for it in items:
					OrderItem.objects.create(order=order, product=it['product'], quantity=it['quantity'], price=it['product'].price)
				# decrement stock
				for product, qty in products_to_update:
					if product.quantity is not None:
						product.quantity = max(0, product.quantity - qty)
						product.save()
				# clear cart
				_save_cart(request, {})
				messages.success(request, 'Pedido realizado com sucesso!')
				return redirect('orders:order_success', order_id=order.id)
		except Exception:
			messages.error(request, 'Ocorreu um erro ao processar seu pedido.')
			return redirect('cart_detail')

	return render(request, 'orders/checkout.html', {'items': items, 'total': total})


@login_required
def order_success(request, order_id):
	order = Order.objects.filter(id=order_id, customer__user=request.user).first()
	if not order:
		messages.error(request, 'Pedido não encontrado.')
		return redirect('home')
	return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_list(request):
	# only customers can view their orders
	customer_profile = getattr(request.user, 'customer_profile', None)
	if not customer_profile:
		messages.error(request, 'Apenas clientes podem visualizar pedidos.')
		return redirect('home')
	orders = Order.objects.filter(customer=customer_profile).order_by('-created_at')
	return render(request, 'orders/order_list.html', {'orders': orders})
