from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.urls import reverse
from django.contrib import messages


def _get_cart(request):
	return request.session.get('cart', {})


def _save_cart(request, cart):
	request.session['cart'] = cart
	request.session.modified = True


def add_to_cart(request, slug):
	product = get_object_or_404(Product, slug=slug)
	cart = _get_cart(request)
	qty = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
	pid = str(product.id)
	cart[pid] = cart.get(pid, 0) + qty
	_save_cart(request, cart)
	messages.success(request, f'✅ Produto "{product.name}" adicionado ao carrinho ({qty}x).')
	# Redirecionar para a página de detalhes ou carrinho conforme POST 'next'
	next_page = request.POST.get('next')
	if next_page:
		return redirect(next_page)
	return redirect('cart_detail')


def remove_from_cart(request, slug):
	product = get_object_or_404(Product, slug=slug)
	cart = _get_cart(request)
	pid = str(product.id)
	if pid in cart:
		del cart[pid]
		_save_cart(request, cart)
		messages.success(request, f'Produto "{product.name}" removido do carrinho.')
	return redirect('cart_detail')


def update_cart(request):
	if request.method != 'POST':
		return redirect('cart_detail')
	cart = _get_cart(request)
	for pid, qty in request.POST.items():
		if not pid.startswith('qty_'):
			continue
		prod_id = pid.split('qty_')[1]
		try:
			q = int(qty)
		except ValueError:
			q = 0
		if q <= 0:
			cart.pop(prod_id, None)
		else:
			cart[prod_id] = q
	_save_cart(request, cart)
	messages.success(request, 'Carrinho atualizado.')
	return redirect('cart_detail')


def cart_detail(request):
	cart = _get_cart(request)
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
	return render(request, 'cart/cart_detail.html', {'items': items, 'total': total})
