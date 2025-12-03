# 💳 Cartões de Teste - Stripe Integration

**Ambiente:** Stripe Test Mode  
**Válido para:** Testes locais de desenvolvimento  

---

## ✅ Cartões de Sucesso

### 1. **Cartão Padrão (Recomendado)**
```
Número:     4242 4242 4242 4242
Data:       12/25 (ou qualquer mês/ano futuro)
CVC:        123 (qualquer 3 dígitos)
CEP:        12345 (qualquer 5 dígitos)
Nome:       Seu Nome de Teste
```
**Resultado:** ✅ Pagamento aceito com sucesso

---

### 2. **Cartão Visa**
```
Número:     4000 0566 5566 5556
Data:       12/25
CVC:        123
```
**Resultado:** ✅ Pagamento bem-sucedido

---

### 3. **Cartão Mastercard**
```
Número:     5555 5555 5555 4444
Data:       12/25
CVC:        123
```
**Resultado:** ✅ Pagamento bem-sucedido

---

### 4. **Cartão American Express**
```
Número:     3782 822463 10005
Data:       12/25
CVC:        1234 (4 dígitos para AMEX)
```
**Resultado:** ✅ Pagamento bem-sucedido

---

### 5. **Cartão Discover**
```
Número:     6011 1111 1111 1117
Data:       12/25
CVC:        123
```
**Resultado:** ✅ Pagamento bem-sucedido

---

## ❌ Cartões de Falha

### 1. **Cartão Recusado (Generic Decline)**
```
Número:     4000 0000 0000 0002
Data:       12/25
CVC:        123
```
**Resultado:** ❌ Pagamento recusado  
**Código de Erro:** card_declined

---

### 2. **Saldo Insuficiente**
```
Número:     4000 0000 0000 9995
Data:       12/25
CVC:        123
```
**Resultado:** ❌ Saldo insuficiente  
**Código de Erro:** insufficient_funds

---

### 3. **Cartão Expirado**
```
Número:     4000 0000 0000 0069
Data:       12/25
CVC:        123
```
**Resultado:** ❌ Cartão expirado  
**Código de Erro:** expired_card

---

### 4. **CVC Inválido**
```
Número:     4000 0000 0000 0127
Data:       12/25
CVC:        123
```
**Resultado:** ❌ CVC inválido  
**Código de Erro:** incorrect_cvc

---

### 5. **Dados de Teste Inválidos**
```
Número:     4000 0000 0000 0341
Data:       12/25
CVC:        123
```
**Resultado:** ❌ Informação de teste inválida  
**Código de Erro:** testing_mode_live_card

---

## 🧪 Cartões para Cenários Específicos

### Autenticação 3D Secure (3DS)

#### Requer Autenticação:
```
Número:     4000 2500 3010 0009
Data:       12/25
CVC:        123
```
**Resultado:** Requer confirmação 3DS (popup)

---

#### Falha Automática na Autenticação:
```
Número:     4000 0002 5000 0003
Data:       12/25
CVC:        123
```
**Resultado:** Autenticação falha

---

## 📱 Testes no Checkout Solar Store

### Passo a Passo:

1. **Acessar checkout:**
   ```
   http://localhost:8000/orders/checkout/
   ```

2. **Preencher dados do cliente:**
   ```
   Nome: Seu Nome Teste
   Email: teste@example.com
   Endereço: Rua Teste, 123
   ```

3. **Selecionar um cartão de teste:**
   - Use a tabela acima conforme o cenário

4. **Preencher dados do cartão no formulário:**
   ```
   Número: [Cartão escolhido]
   Validade: 12/25
   CVC: 123
   ```

5. **Clicar "Finalizar Compra"**

6. **Verificar resultado:**
   - ✅ Sucesso → Página de confirmação
   - ❌ Erro → Mensagem de erro com código

---

## 🔍 Verificar Transações no Stripe

### Dashboard Stripe:

1. Acesse: https://dashboard.stripe.com/test/payments
2. Login com sua conta Stripe
3. Procure pela transação (por data/valor)
4. Veja detalhes e log de erros

---

## 📊 Recomendações de Teste

### Cenários Obrigatórios:

- [ ] Teste com cartão válido (4242...)
- [ ] Teste com cartão recusado (4000 0000 0000 0002)
- [ ] Teste com CVC inválido
- [ ] Teste com data expirada
- [ ] Teste com 3D Secure
- [ ] Verifique email de confirmação
- [ ] Verifique webhook no Stripe

---

## 🔐 Segurança

### ⚠️ NUNCA fazer isso em PRODUÇÃO:

```python
# ❌ ERRADO - Cartões reais em teste
card_number = input("Digite o número do cartão: ")

# ✅ CORRETO - Usar Stripe Elements (tokenização)
# Stripe Elements criptografa dados automaticamente
```

---

## 🧩 Integração com o Projeto

### Arquivo: `payments/views.py`

```python
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    # Stripe processa automaticamente
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        success_url='...',
        cancel_url='...',
    )
    return redirect(session.url)
```

### O fluxo de teste:

```
1. Cliente acessa /orders/checkout/
2. Preenche dados (nome, email, endereço)
3. Insere número do cartão
4. Clica "Pagar"
5. Stripe.checkout.Session.create() é chamado
6. Redireciona para página Stripe (segura)
7. Cliente confirma pagamento
8. Webhook atualiza status no banco
9. Confirmação por email
```

---

## 📞 Webhook de Teste

### Para testar webhooks localmente:

```bash
# 1. Instalar Stripe CLI
# https://stripe.com/docs/stripe-cli

# 2. Fazer login
stripe login

# 3. Escutar eventos
stripe listen --forward-to localhost:8000/payments/webhook/

# 4. Fazer teste de pagamento
# O webhook será automaticamente chamado
```

---

## 🎯 Exemplos de Teste Prático

### Teste 1: Pagamento Bem-Sucedido

```bash
1. Criar produto de teste (R$ 100.00)
2. Adicionar ao carrinho
3. Ir para checkout
4. Usar cartão: 4242 4242 4242 4242
5. Confirmar pagamento
✅ Resultado esperado: Pedido criado com status "processing"
```

---

### Teste 2: Pagamento Recusado

```bash
1. Mesmo processo acima
2. Usar cartão: 4000 0000 0000 0002
3. Confirmar pagamento
❌ Resultado esperado: Erro "card_declined"
✅ Usuário pode tentar novamente
```

---

### Teste 3: Validação de Erro

```bash
1. Ir para checkout
2. Usar cartão: 4000 0000 0000 0069 (expirado)
3. Confirmar pagamento
❌ Resultado esperado: Erro "expired_card"
✅ Mensagem clara no formulário
```

---

## 📋 Checklist de Testes

- [ ] Pagamento com sucesso (4242...)
- [ ] Pagamento recusado (4000...)
- [ ] Email de confirmação recebido
- [ ] Pedido aparece no Dashboard
- [ ] Status do pedido atualizado
- [ ] Webhook funcionando
- [ ] Página de sucesso exibida
- [ ] Carrinho limpo após pagamento
- [ ] Histórico de pedidos atualizado
- [ ] Admin pode ver transação

---

## 🚀 Pronto para Testar!

Você pode agora:

1. ✅ Acessar http://localhost:8000/orders/checkout/
2. ✅ Usar cartão **4242 4242 4242 4242**
3. ✅ Data **12/25** e CVC **123**
4. ✅ Clicar "Finalizar Compra"
5. ✅ Ver pagamento ser processado

---

## 📚 Referências

- [Stripe Test Cards Official](https://stripe.com/docs/testing)
- [Stripe Test Mode](https://stripe.com/docs/test-mode)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [Webhook Testing](https://stripe.com/docs/webhooks/testing)

---

**Criado em:** Dezembro 2025  
**Versão:** 1.0.0  
**Status:** ✅ Pronto para uso

---

💡 **Dica:** Mantenha este arquivo como referência durante desenvolvimento!
