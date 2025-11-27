from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create-session/', views.create_payment_session, name='create_session'),
    path('success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('cancel/<int:order_id>/', views.payment_cancel, name='payment_cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
