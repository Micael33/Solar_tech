from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SellerRegisterForm, CustomerRegisterForm


def seller_register(request):
    if request.method == 'POST':
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('seller_dashboard')
    else:
        form = SellerRegisterForm()
    return render(request, 'accounts/seller_register.html', {'form': form})


def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('customer_dashboard')
    else:
        form = CustomerRegisterForm()
    return render(request, 'accounts/customer_register.html', {'form': form})


@login_required
def seller_dashboard(request):
    """Dashboard para vendedores"""
    seller_profile = getattr(request.user, 'seller_profile', None)
    if not seller_profile:
        return redirect('login')
    
    products = seller_profile.products.all()
    return render(request, 'accounts/seller_dashboard.html', {
        'products': products,
        'products_count': products.count()
    })


@login_required
def customer_dashboard(request):
    """Dashboard para clientes"""
    customer_profile = getattr(request.user, 'customer_profile', None)
    if not customer_profile:
        return redirect('login')
    
    return render(request, 'accounts/customer_dashboard.html')