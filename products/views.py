from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required


def product_list(request):
    qs = Product.objects.filter(quantity__gt=0)
    query = request.GET.get('q')
    if query:
        qs = qs.filter(name__icontains=query)
    return render(request, 'products/product_list.html', {'products': qs})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # Verificar se o usuário atual é vendedor
    is_seller = hasattr(request.user, 'seller_profile') and request.user.is_authenticated
    return render(request, 'products/product_detail.html', {'product': product, 'is_seller': is_seller})

@login_required
def product_create(request):
    # Só vendedor pode criar — verificamos se tem seller_profile
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller_register')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.seller = request.user.seller_profile
            prod.save()
            return redirect('product_detail', slug=prod.slug)
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {'form': form})


@login_required
def product_edit(request, slug):
    """Editar produto (apenas o vendedor proprietário pode editar)"""
    product = get_object_or_404(Product, slug=slug)
    
    # Verificar se o usuário é o vendedor proprietário
    if not hasattr(request.user, 'seller_profile') or product.seller != request.user.seller_profile:
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {'form': form, 'product': product, 'is_edit': True})