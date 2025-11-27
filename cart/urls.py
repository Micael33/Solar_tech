from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart, name='update_cart'),
]
