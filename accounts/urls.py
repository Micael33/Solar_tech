from django.urls import path
from . import views

urlpatterns = [
    path('seller/register/', views.seller_register, name='seller_register'),
    path('customer/register/', views.customer_register, name='customer_register'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
]
