from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SellerProfile, CustomerProfile


class SellerRegisterForm(UserCreationForm):
    company_name = forms.CharField(label='Razão Social / Nome da Empresa', max_length=200)
    cnpj = forms.CharField(label='CNPJ', max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'company_name', 'cnpj')

    def save(self, commit=True):
        user = super().save(commit=commit)
        # create seller profile
        SellerProfile.objects.create(
            user=user,
            company_name=self.cleaned_data['company_name'],
            cnpj=self.cleaned_data['cnpj']
        )
        return user


class CustomerRegisterForm(UserCreationForm):
    cpf = forms.CharField(label='CPF', max_length=14)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'cpf')

    def save(self, commit=True):
        user = super().save(commit=commit)
        CustomerProfile.objects.create(
            user=user,
            cpf=self.cleaned_data['cpf']
        )
        return user
