# ❓ FAQ - Perguntas Frequentes

## 🚀 Instalação e Setup

### P: Como instalar o projeto?
**R:** Siga este checklist:
```bash
# 1. Clonar
git clone https://github.com/seu-usuario/solar-store.git
cd solar-store

# 2. Virtual env
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Dependências
pip install -r requirements.txt

# 4. Variáveis
# Criar .env com STRIPE_KEYS etc

# 5. Banco de dados
python manage.py migrate

# 6. Rodar
python manage.py runserver
```
Acesse: http://127.0.0.1:8000

---

### P: Dá erro "No module named 'stripe'"?
**R:** Instale:
```bash
pip install stripe==14.0.1
```

---

### P: Qual versão de Python preciso?
**R:** Python 3.11 ou superior. Verifique:
```bash
python --version
```

---

### P: O que é o arquivo `.env`?
**R:** Arquivo com variáveis sensíveis (nunca commitar):
```
SECRET_KEY=sua-chave
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

---

## 👤 Autenticação

### P: Como registrar um novo usuário?
**R:** Clique em "Registrar" → escolha Vendedor/Cliente → preencha dados

---

### P: Qual é a diferença entre Vendedor e Cliente?
**R:**
- **Vendedor:** Cria e vende produtos
- **Cliente:** Compra produtos de vendedores

---

### P: Esqueci a senha, como recupero?
**R:** Clique em "Esqueceu senha?" na página de login
(Email transacional precisa ser configurado)

---

### P: Como criar usuários de teste?
**R:** Via Django shell:
```bash
python manage.py shell

from django.contrib.auth.models import User
from accounts.models import CustomerProfile

user = User.objects.create_user(
    username='test',
    email='test@example.com',
    password='123456'
)

CustomerProfile.objects.create(
    user=user,
    cpf='12345678900'
)
```

---

## 📦 Produtos

### P: Como criar um produto?
**R:** 
1. Registre como Vendedor
2. Acesse Dashboard
3. Clique "Novo Produto"
4. Preencha: nome, preço, descrição, quantidade
5. Clique "Criar"

---

### P: Posso editar um produto após criar?
**R:** Sim! Vendedor acessa Dashboard → produto → "Editar"

---

### P: Como faço upload de imagem?
**R:** No formulário de criar/editar produto, há campo "Imagem"
- Aceita: JPG, PNG, GIF
- Tamanho máx: 5MB (configurável)

---

### P: Como buscar produtos?
**R:** Na página `/products/` há caixa de busca
- Busca por nome e descrição

---

## 🛒 Carrinho

### P: Onde está meu carrinho?
**R:** Clique no ícone 🛒 no topo da página
ou acesse `/cart/`

---

### P: Como adicionar ao carrinho?
**R:** 
1. Vá para detalhe do produto
2. Digite a quantidade
3. Clique "Adicionar ao Carrinho"

---

### P: Posso aumentar/diminuir quantidade?
**R:** Sim, na página do carrinho há inputs de quantidade

---

### P: Meu carrinho ficou vazio, por quê?
**R:** Possíveis razões:
- Limpou cookies do navegador
- Expirou a sessão
- Fez logout

---

## 💳 Pagamentos

### P: Quais cartões posso usar?
**R:** Aceita todos os cartões principais:
- Visa
- Mastercard
- American Express
- Elo

---

### P: Posso testar pagamentos sem dinheiro real?
**R:** Sim! Use dados de teste do Stripe:
```
Cartão: 4242 4242 4242 4242
Data: 12/25 (qualquer futura)
CVC: 123
```

---

### P: Meu pagamento falhou, como resolvo?
**R:** 
1. Verifique se dados estão corretos
2. Tente outro cartão
3. Contate seu banco
4. Tente novamente em alguns minutos

---

### P: Recebi email de confirmação após pagar?
**R:** Você deveria! Se não recebeu:
1. Verifique spam/lixo
2. Verifique se email está correto
3. Acesse Dashboard → Meus Pedidos

---

### P: Posso reembolsar um pedido?
**R:** Contate suporte. Reembolsos processados em 3-5 dias úteis

---

## 📊 Dashboard

### P: O que vejo no Dashboard Cliente?
**R:**
- Informações do perfil
- Pedidos recentes
- Estatísticas (total gasto)
- Atalhos (Explorar, Carrinho, Pedidos)

---

### P: O que vejo no Dashboard Vendedor?
**R:**
- Produtos que criei
- Botões Editar/Deletar
- Pedidos recentes
- Estatísticas (total produtos, vendas)

---

### P: Como deletar um produto?
**R:** No Dashboard Vendedor, clique "Deletar" no produto
(Cuidado: não há como desfazer!)

---

## 🐛 Problemas e Erros

### P: Erro "CSRF verification failed"?
**R:** Isso é de segurança. Tente:
1. Limpar cookies
2. Fazer logout/login
3. Se em produção, verificar CSRF_TRUSTED_ORIGINS

---

### P: Erro "Page not found (404)"?
**R:** A página não existe. Verifique:
- URL está correta
- Produto existe
- Não há typo

---

### P: Erro de banco de dados?
**R:** Tente:
```bash
python manage.py migrate
python manage.py makemigrations
```

---

### P: Servidor não inicia?
**R:** Verifique erros:
```bash
python manage.py check
```

---

### P: Imagens não aparecem?
**R:** Tente:
```bash
python manage.py collectstatic
```

---

## 🚀 Deployment

### P: Como fazer deploy para produção?
**R:** Ver [DOCUMENTATION.md → Deployment](./DOCUMENTATION.md#-deployment-e-produção)

Passos básicos:
1. Usar banco PostgreSQL
2. DEBUG=False
3. Configurar ALLOWED_HOSTS
4. Usar WSGI server (Gunicorn)
5. Proxy reverso (Nginx)
6. SSL (Let's Encrypt)

---

### P: Posso usar Heroku?
**R:** Sim! Heroku oferece free tier:
```bash
heroku login
heroku create solar-store
git push heroku main
```

---

### P: Preciso mudar para PostgreSQL?
**R:** Recomendado para produção (SQLite é desenvolvimento)

```bash
pip install psycopg2
# Configurar em settings.py
# Fazer migrations
```

---

## 💻 Desenvolvimento

### P: Como contribuir com código?
**R:**
1. Fork o repositório
2. Create branch: `git checkout -b feature/sua-feature`
3. Fazer mudanças
4. Commit: `git commit -m "feat: descrição"`
5. Push: `git push origin feature/sua-feature`
6. Pull Request no GitHub

Ver [DEVELOPMENT.md](./DEVELOPMENT.md) para detalhes

---

### P: Como rodar testes?
**R:**
```bash
python manage.py test
# ou específico:
python manage.py test products.tests
```

---

### P: Como checar cobertura de testes?
**R:**
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Abre em browser
```

---

### P: Como usar Django shell?
**R:**
```bash
python manage.py shell

# Agora você pode:
>>> from products.models import Product
>>> products = Product.objects.all()
>>> products.count()
```

---

## 📚 Documentação

### P: Onde está a documentação?
**R:** 
- [INDEX.md](./INDEX.md) - Índice completo
- [README.md](./README.md) - Setup e features
- [DOCUMENTATION.md](./DOCUMENTATION.md) - Tudo técnico
- [API_REFERENCE.md](./API_REFERENCE.md) - Endpoints
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Dev guide

---

### P: Qual doc devo ler primeiro?
**R:** Nesta ordem:
1. README.md
2. QUICK_START.md
3. DOCUMENTATION.md
4. Seu documento específico

---

## 🎨 Design e CSS

### P: Como é a paleta de cores?
**R:** Tema "Energia Solar":
- Amarelo: #f7b733
- Laranja: #fc4a1a
- Azul: #003f7f
- Azul Claro: #1976d2
- Cinza: #6e6e6e
- Branco: #fafafa

---

### P: Onde estão os CSS?
**R:** `static/css/`
- base.css (global)
- home.css (homepage)
- auth.css (login)
- products.css (catálogo)
- cart.css (carrinho)
- checkout.css (checkout)
- orders.css (pedidos)
- dashboard.css (dashboards)

---

### P: Como adicionar novo CSS?
**R:** 
1. Criar arquivo `static/css/novo.css`
2. Adicionar em template: `<link rel="stylesheet" href="{% static 'css/novo.css' %}">`

---

## 🏗️ Arquitetura

### P: Qual é a estrutura de pastas?
**R:**
```
solar-store/
├── accounts/        → Autenticação
├── products/        → Produtos
├── cart/           → Carrinho
├── orders/         → Pedidos
├── payments/       → Pagamentos
├── static/         → CSS, JS, imagens
├── templates/      → HTML
└── solar_store/    → Configurações
```

---

### P: Quantas tabelas de banco de dados?
**R:** Principais (excluindo Django auth):
- User (Django)
- SellerProfile
- CustomerProfile
- Product
- Order
- OrderItem
- Payment

Totalizando ~7 modelos

---

### P: Posso adicionar uma nova app?
**R:** Sim!
```bash
python manage.py startapp nova_app

# Depois:
# 1. Adicionar em INSTALLED_APPS (settings.py)
# 2. Criar models.py
# 3. Criar views.py
# 4. Criar urls.py
# 5. Incluir em urls.py principal
# 6. Fazer migrações
```

---

## 🔐 Segurança

### P: Minha senha é segura?
**R:** Django usa hash bcrypt/PBKDF2, muito seguro

---

### P: Dados de cartão são armazenados?
**R:** Não! Stripe cuida disso. Nunca processamos dados de cartão

---

### P: Como são as variáveis sensíveis protegidas?
**R:** 
- Em `.env` (git-ignored)
- Nunca em commits
- Variáveis de ambiente em produção

---

## 📞 Suporte

### P: Como reportar um bug?
**R:** 
1. Abra issue no GitHub
2. Descreva o problema
3. Como reproduzir
4. Screenshots (se possível)

---

### P: Como sugerir uma feature?
**R:** 
1. Abra Discussion no GitHub
2. Descreva a feature
3. Explique por quê seria útil

---

### P: Preciso de ajuda com Stripe?
**R:** 
- [STRIPE_SETUP.md](./STRIPE_SETUP.md)
- [Documentação Stripe](https://stripe.com/docs)
- [Comunidade Stripe](https://stripe.com/community)

---

## 🎓 Aprendizado

### P: Posso aprender Django com este projeto?
**R:** Sim! É um ótimo projeto educacional com:
- Modelos bem estruturados
- Views boas práticas
- Autenticação
- Integração com API (Stripe)
- Testes

---

### P: Há exemplos de código?
**R:** Sim! Ver:
- [DOCUMENTATION.md → Exemplos](./DOCUMENTATION.md#-exemplos-de-código)
- [DEVELOPMENT.md → Padrões](./DEVELOPMENT.md#-padrões-de-código)

---

### P: Posso usar este projeto como template?
**R:** Sim! Ele foi pensado como referência
- Está sob licença MIT
- Pode modificar
- Pode comercializar
- Apenas manter atribuição

---

## 📊 Performance

### P: Por que o site fica lento?
**R:** Possíveis causas:
1. Muitos produtos (use paginação)
2. Imagens grandes (otimize)
3. Queries N+1 (use select_related)
4. Cache não configurado

Ver [DEVELOPMENT.md → Performance](./DEVELOPMENT.md#-performance)

---

### P: Como otimizar banco de dados?
**R:**
```python
# Ruim - N+1 queries
for product in products:
    print(product.seller.name)

# Bom - select_related
products = Product.objects.select_related('seller')
```

---

## 🌐 Localização

### P: Como adicionar outro idioma?
**R:** Django suporta i18n:
```python
from django.utils.translation import gettext_lazy as _

name = _("Produto")  # Marcado para tradução
```

---

## 🤔 Ainda com Dúvidas?

### Checklist:
- [ ] Leu o README.md?
- [ ] Leu DOCUMENTATION.md?
- [ ] Procurou neste FAQ?
- [ ] Procurou no Google?
- [ ] Consultou a doc do Django?

Se ainda estiver preso:
1. Abra uma **Issue** no GitHub
2. Descreva o problema detalhadamente
3. Inclua logs de erro
4. Inclua seu ambiente (OS, Python version)

---

## 📝 Última Atualização

**Data:** Dezembro 2025  
**Versão:** 1.0.0

Alguma pergunta não está respondida? Abra uma issue e vamos adicionar!

---

**Desenvolvido com ❤️ para facilitar a jornada! ☀️**
