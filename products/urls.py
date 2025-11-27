from django.urls import path
from . import views


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('novo/', views.product_create, name='product_create'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    ]