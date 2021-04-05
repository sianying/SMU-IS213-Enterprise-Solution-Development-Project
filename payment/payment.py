import os
import math
from flask import Flask, jsonify, request
import json
import requests
import stripe
from flask_cors import CORS

# This is a sample test API key. Sign in to see examples pre-filled with your key.
stripe.api_key = 'sk_test_51IX1pfEh2v7rRS8AcPlo5xnom5URyB0pGOpVahhgBjIUWLThrnp864myMWWOj4Hbr6hxVJaDBiRI657dnwFOshmS008gjCP4fb'

app = Flask(__name__)

CORS(app)

#checkout with payment
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    post_data = json.loads(request.data)
    delivery_item = post_data['deliveryItem']
    description = post_data['description']
    size = post_data['size']
    weight = post_data['weight']
    # print(post_data)
    # delivery_item = data["price_data"]["product_data"]["name"]
    # size = post_data["size"]
    # return data
    #price processing
    pricing = {"Small": 3, "Medium": 6, "Large": 9} 
    for key in pricing:
        if size == key:
            unit_amount = int(pricing[size] * float(weight)*100)
    data = {
        "price_data": {"currency": "sgd", 
                    "product_data": {"name": delivery_item}, 
                    "unit_amount": unit_amount},
        "quantity": 1
    }

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                data
                # {
                # "price_data": {"currency": "sgd", "product_data": {"name": "T-shirt"}, "unit_amount": 100},
                # "quantity": 1
                # }
        ],
            mode="payment",
            success_url= "http://localhost/ESD/UI(General)/payment/success.html" + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost/ESD/Project/cancel.html"
        )
        return jsonify({'id': checkout_session.id})
        

    except Exception as e:
        return jsonify(error=str(e)), 403

#return checkout information with session id
@app.route('/checkout_session/<string:session_id>', methods=['GET'])
def get_checkout_session(session_id):
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    return jsonify({
        "payment_status": checkout_session.payment_status,
        "amount_total": checkout_session.amount_total,
        "currency": checkout_session.currency,
        "customer": checkout_session.customer,
        "customer_email": checkout_session.customer_details.email,
        "metadata": checkout_session.metadata
    })


if __name__ == '__main__':
    app.run(port=4242, debug=True)