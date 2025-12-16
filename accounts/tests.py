from django.test import TestCase
from django.contrib.auth.models import User
from .forms import CustomerRegisterForm, SellerRegisterForm
from .models import CustomerProfile, SellerProfile


class CustomerRegistrationTests(TestCase):
	def test_duplicate_cpf_shows_form_error(self):
		# Cria um cliente pré-existente
		u = User.objects.create_user(username='existing', password='Password123!')
		CustomerProfile.objects.create(user=u, cpf='111.111.111-11')

		form = CustomerRegisterForm({
			'username': 'newuser',
			'email': 'newuser@example.com',
			'password1': 'Password123!',
			'password2': 'Password123!',
			'cpf': '111.111.111-11',
		})

		self.assertFalse(form.is_valid())
		self.assertIn('cpf', form.errors)


class SellerRegistrationTests(TestCase):
	def test_duplicate_cnpj_shows_form_error(self):
		u = User.objects.create_user(username='seller', password='Password123!')
		SellerProfile.objects.create(user=u, cnpj='12.345.678/0001-99', company_name='ACME')

		form = SellerRegisterForm({
			'username': 'seller2',
			'email': 'seller2@example.com',
			'password1': 'Password123!',
			'password2': 'Password123!',
			'company_name': 'Other',
			'cnpj': '12.345.678/0001-99',
		})

		self.assertFalse(form.is_valid())
		self.assertIn('cnpj', form.errors)
