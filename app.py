import os
from flask import Flask, render_template, abort, redirect, request
import stripe
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import dotenv
from pyngrok import ngrok
from datetime import datetime

load_dotenv()


# Criar instância do aplicativo Flask
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Configurar URL do banco de dados

db = SQLAlchemy(app)  # Inicializar a extensão SQLAlchemy com o aplicativo Flask

# Definir o modelo do banco de dados
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pagador = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.now())

with app.app_context():  # Criar contexto de aplicação
    db.create_all()  # Criar tabelas no banco de dados

stripe.api_key = os.environ['STRIPE_SECRET_KEY']

products = {
    'Suporte total': {
        'name': 'Pack full - Aprenda Python',
        'price': 200000,
    },
    'Suporte por horas': {
        'name': 'Pack horas - Aprenda Python',
        'price': 10000,
        'por': 'hora',
        'adjustable_quantity': {
            'enabled': True,
            'minimum': 1,
            'maximum': 15,
        },
    },
}



@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/order/<product_id>', methods=['POST'])
def order(product_id):
    if product_id not in products:
        abort(404)

    product = products[product_id]

    line_item = {
        'price_data': {
            'product_data': {
                'name': product['name'],
            },
            'unit_amount': product['price'],
            'currency': 'BRL',
        },
        'quantity': 1,
        'adjustable_quantity': product.get('adjustable_quantity', {'enabled': False}),
    }

    checkout_session = stripe.checkout.Session.create(
        line_items=[line_item],
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + 'order/success',
        cancel_url=request.host_url + 'order/cancel',
    )
    return redirect(checkout_session.url)

@app.route('/order/success')
def success():
    return render_template('success.html')

@app.route('/order/cancel')
def cancel():
    return render_template('cancel.html')

@app.route('/event', methods=['POST'])
def new_event():
    with app.app_context():  # Criar contexto de aplicação
        event = None
        payload = request.data
        signature = request.headers['STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(payload, signature, os.environ['STRIPE_WEBHOOK_SECRET'])
        except Exception as e:
            print(e)
            abort(400)

        if event['type'] == 'checkout.session.completed':
            session = stripe.checkout.Session.retrieve(
                event['data']['object'].id, expand=['line_items'])
            #print(f'Sale to {session.customer_details.email}:')
            for item in session.line_items.data:
                #print (item)
                print (session.customer_details)
                # Criar instância do modelo Produto e salvar no banco de dados
                produto = Produto(pagador = session.customer_details.name ,nome=item.description, valor=item.amount_total/100, email=session.customer_details.email)
                db.session.add(produto)
                db.session.commit()
                """ print(f'  - {item.quantity} {item.description} '
                      f'${item.amount_total/100:.02f} {item.currency.upper()}') """

    return {'success': True}


public_url = ngrok.connect(5000)

# Acessar a URL pública gerada pelo ngrok
print("URL pública do ngrok: ", public_url)

if __name__ == '__main__':
    app.run()