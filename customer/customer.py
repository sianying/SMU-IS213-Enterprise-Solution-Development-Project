from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os
from os import environ

app = Flask(__name__)
CORS(app)

HOST = "0.0.0.0"
PORT = 5002


app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@127.0.0.1:3306/customer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customer'

    customer_ID = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(64), nullable=False)
    customer_email = db.Column(db.String(128), nullable=False)
    customer_mobile = db.Column(db.Integer, nullable=False)
    customer_teleID = db.Column(db.String(20), nullable=True)
    tele_chat_ID = db.Column(db.String(15), nullable=True)

    def __init__(self, customer_ID, customer_name, customer_email, customer_mobile, customer_teleID, tele_chat_ID):
        self.customer_ID = customer_ID
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_mobile = customer_mobile
        self.customer_teleID = customer_teleID
        self.tele_chat_ID = tele_chat_ID

    def json(self):
        return {
            "customer_ID": self.customer_ID,
            "customer_name": self.customer_name, 
            "customer_email": self.customer_email, 
            "customer_mobile": self.customer_mobile, 
            "customer_teleID": self.customer_teleID,
            "tele_chat_ID": self.tele_chat_ID
        }
        

# 1. return a specific customer
@app.route("/customer/<int:customer_ID>")
def find_by_customer_ID(customer_ID):
    customer = Customer.query.filter_by(customer_ID=customer_ID).first()
    if customer:
        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Customer not found."
        }
    ), 404

# 2. create a new customer, customer_ID will be auto incremented 
# pass in POST request, except customer_ID 
@app.route("/customer", methods=['POST'])
def create_customer():

    recent_customer = Customer.query.order_by(Customer.customer_ID.desc()).first()
    if not (recent_customer):
        customer_ID = 1001
    else:
        customer_ID = recent_customer.customer_ID + 1

    data = request.get_json()
    customer = Customer(customer_ID, **data)

    try:
        db.session.add(customer)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "customer_ID": customer_ID
                },
                "message": "An error occurred creating the customer."
            }
        ), 500
    
    return jsonify(
        {
            "code": 201,
            'data': customer.json()
        }
    ), 201


# 3. update customer's chat_ID using tele_ID
@app.route("/customer/<string:customer_teleID>", methods=['PUT'])
def update_customer_chatID(customer_teleID):
    customer = Customer.query.filter_by(customer_teleID=customer_teleID).first()
    if not (customer):
        return jsonify({
                "code": 404,
                "data": {
                    "customer_teleID": customer_teleID
                },
                "message": "Customer does not exist."
            }), 404

    data = request.get_json()
    #chat_ID is stored as varchar/string in db, hence, convert the incoming to str for comparison
    input_tele_chat_ID = str(data['tele_chat_ID'])

    if customer.tele_chat_ID == input_tele_chat_ID:
        return jsonify({
            "code": 400,
                "data": {
                    "customer_teleID": customer_teleID
                },
            "message": "Customer has already registered his chat_ID."
        }), 400

    try:
        customer.tele_chat_ID = input_tele_chat_ID
        db.session.commit()

    except:
        return jsonify({
                "code": 500,
                "data": {
                    "customer_teleID": customer_teleID
                },
                "message": "An error occurred updating the customer."
            }), 500
    
    return jsonify({
            "code": 202,
            'data': customer.json(),
            "message": "Customer chat_ID has successfully been updated."
        }), 202


if __name__ == '__main__':
    print("This is flask " + os.path.basename(__file__) + " for Customer details...")
    print(os.path.basename(__file__) + " is running on " + str(HOST) + ":" + str(PORT) + " ...")
    app.run(host=HOST, port=PORT, debug=True)
