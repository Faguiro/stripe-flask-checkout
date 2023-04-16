# Stripe-Flask-Checkout
Este é um subsistema criado em Flask para processar pagamentos usando a API do Stripe. O subsistema inclui um processo de checkout simples, que permite aos usuários realizar pagamentos de forma rápida e segura.

# Requisitos:
Antes de usar este subsistema, certifique-se de ter os seguintes requisitos instalados em sua máquina:

Python 3
Flask
Stripe Python Library
Jinja2

# Instalação

Para instalar o subsistema, siga os seguintes passos:

1 - Clone o repositório em sua máquina local:

```
git clone https://github.com/Faguiro/stripe-flask-checkout.git
```
Instale as dependências necessárias utilizando o comando:
```
pip install -r requirements.txt
```
Configure sua conta no Stripe e obtenha as chaves API e as chaves secretas.

Insira suas chaves no arquivo config.py na pasta stripe_checkout.

# Uso
Para usar o subsistema, execute o arquivo app.py na pasta stripe_checkout:

```
python app.py
```
Acesse o checkout através do navegador usando a URL: 
```
http://localhost:5000/checkout.
```
O subsistema agora está pronto para uso e os usuários podem realizar pagamentos com segurança usando a API do Stripe.

# Contribuição
Contribuições são sempre bem-vindas. Se você deseja contribuir com o subsistema, siga as diretrizes de contribuição na pasta CONTRIBUTING.md.

# Licença
Este subsistema é licenciado sob a Licença MIT. Consulte o arquivo LICENSE para obter mais informações.