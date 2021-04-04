from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os
from os import environ

app = Flask(__name__)
CORS(app)

HOST = "0.0.0.0"
PORT = 5002


# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/customer'
#there is a need for authentication to the database using root (user) and pass(if there is any)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customer'

    customer_ID = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(64), nullable=False)
    customer_email = db.Column(db.String(128), nullable=False)
    customer_mobile = db.Column(db.Integer, nullable=False)
    customer_teleID = db.Column(db.String(20), nullable=True)

    def __init__(self, customer_ID, customer_name, customer_email, customer_mobile, customer_teleID):
        self.customer_ID = customer_ID
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_mobile = customer_mobile
        self.customer_teleID = customer_teleID

    def json(self):
        return {
            "customer_ID": self.customer_ID,
            "customer_name": self.customer_name, 
            "customer_email": self.customer_email, 
            "customer_mobile": self.customer_mobile, 
            "customer_teleID": self.customer_teleID
        }

#return all customers
@app.route("/customer")
def get_all():
    customer_list = Customer.query.all()
    if len(customer_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "customers": [customer.json() for customer in customer_list]
                }
            }
        )
    return jsonify(
        {
            "code": 400,
            "message": "There are no customers recorded."
        }
    ), 400

#return a specific customer
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

#create a new customer, customer_ID will be auto incremented 
#pass in POST request, except customer_ID 
@app.route("/customer", methods=['POST'])
def create_customer():

    #shift the checking of existing customer to the registration microservice
    #this is because of the auto increment of the customer_ID
    #customer creation will only be invoked from the Registration CMS
    # if (Customer.query.filter_by(customer_ID=data['customer_ID']).first()):
    #     return jsonify(
    #         {
    #             "code": 400,
    #             "data": {
    #                 "customer_ID": customer_ID,
    #             },
    #             "message": "Customer already exists."
    #         }
    #     ), 400

    #create customer_ID, auto increment
    #if no customer in the database, the incoming customer have an id of 0
    recent_customer = Customer.query.order_by(Customer.customer_ID.desc()).first()
    if not (recent_customer):
        customer_ID = 1000000
    else:
        customer_ID = recent_customer.customer_ID + 1

    data = request.get_json()
    customer = Customer(customer_ID, **data)
    # print(str(customer_ID))

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

#delete a customer
@app.route("/customer/<int:customer_ID>", methods=['DELETE'])
def delete_customer(customer_ID):
    customer = Customer.query.filter_by(customer_ID=customer_ID).first()
    if not (customer):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "customer_ID": customer_ID
                },
                "message": "This customer does not exist."
            }
        ), 400

    try:
        db.session.delete(customer)
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
            "code": 203,
            'data': customer.json(),
            "message": "Customer has successfully been deleted."
        }
    ), 203

#update a customer 
@app.route("/customer/<int:customer_ID>", methods=['PUT'])
def update_customer(customer_ID):
    old_customer = Customer.query.filter_by(customer_ID=customer_ID).first()
    if not (old_customer):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "customer_ID": customer_ID
                },
                "message": "Customer does not exist."
            }
        ), 400

    data = request.get_json()
    new_customer = Customer(customer_ID, **data)

    try:
        # key_list = [attr for attr in dir(old_customer) if "C" in attr and "customer_ID" not in attr]
        # for key in key_list:
        #     old_customer[key] = new_customer[key]

        old_customer.customer_name = new_customer.customer_name
        old_customer.customer_email = new_customer.customer_email
        old_customer.customer_mobile = new_customer.customer_mobile
        old_customer.customer_teleID = new_customer.customer_teleID
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "customer_ID": customer_ID
                },
                "message": "An error occurred updating the customer."
            }
        ), 500
    
    return jsonify(
        {
            "code": 202,
            'data': old_customer.json(),
            "message": "Customer has successfully been updated."
        }
    ), 202


if __name__ == '__main__':
    print("This is flask " + os.path.basename(__file__) + " for Customer details...")
    print(os.path.basename(__file__) + " is running on " + str(HOST) + ":" + str(PORT) + " ...")
    app.run(host=HOST, port=PORT, debug=True)
