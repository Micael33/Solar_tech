from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from products.models import Product


def home(request):
    """Página inicial da aplicação"""
    # Pega os 4 produtos mais recentes
    products = Product.objects.filter(quantity__gt=0).order_by('-created_at')[:4]
    return render(request, 'home.html', {'products': products})


def logout_view(request):
    """View customizada para logout com confirmação"""
    if request.method == 'POST':
        auth_logout(request)
        return redirect('home')
    return render(request, 'registration/logout.html')
