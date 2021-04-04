from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/customer'
#there is a need for authentication to the database using root (user) and pass(if there is any)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customer'

    CID = db.Column(db.Integer, primary_key=True)
    CName = db.Column(db.String(64), nullable=False)
    CEmail = db.Column(db.String(128), nullable=False)
    CMobile = db.Column(db.Integer, nullable=False)
    CTeleID = db.Column(db.String(20), nullable=True)

    def __init__(self, CID, CName, CEmail, CMobile, CTeleID):
        self.CID = CID
        self.CName = CName
        self.CEmail = CEmail
        self.CMobile = CMobile
        self.CTeleID = CTeleID

    def json(self):
        return {
            "CID": self.CID, 
            "CName": self.CName, 
            "CEmail": self.CEmail, 
            "CMobile": self.CMobile, 
            "CTeleID": self.CTeleID
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
@app.route("/customer/<int:CID>")
def find_by_CID(CID):
    customer = Customer.query.filter_by(CID=CID).first()
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

#create a new customer
@app.route("/customer/<int:CID>", methods=['POST'])
def create_customer(CID):
    if (Customer.query.filter_by(CID=CID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "CID": CID
                },
                "message": "Customer already exists."
            }
        ), 400
    
    data = request.get_json()
    customer = Customer(CID, **data)

    try:
        db.session.add(customer)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "CID": CID
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
@app.route("/customer/<int:CID>", methods=['DELETE'])
def delete_customer(CID):
    customer = Customer.query.filter_by(CID=CID).first()
    if not (customer):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "CID": CID
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
                    "CID": CID
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
@app.route("/customer/<int:CID>", methods=['PUT'])
def update_customer(CID):
    old_customer = Customer.query.filter_by(CID=CID).first()
    if not (old_customer):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "CID": CID
                },
                "message": "Customer does not exist."
            }
        ), 400

    data = request.get_json()
    new_customer = Customer(CID, **data)

    try:
        # key_list = [attr for attr in dir(old_customer) if "C" in attr and "CID" not in attr]
        # for key in key_list:
        #     old_customer[key] = new_customer[key]

        old_customer.CName = new_customer.CName
        old_customer.CEmail = new_customer.CEmail
        old_customer.CMobile = new_customer.CMobile
        old_customer.CTeleID = new_customer.CTeleID
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "CID": CID
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


if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
