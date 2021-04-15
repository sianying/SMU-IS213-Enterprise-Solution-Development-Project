from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

import datetime

app = Flask(__name__)
CORS(app)

HOST = '0.0.0.0'
PORT = 5000

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@127.0.0.1:3306/delivery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}
 
db = SQLAlchemy(app)
 
class Delivery(db.Model):
    __tablename__ = 'delivery'

    delivery_ID = db.Column(db.INT(), primary_key=True)
    driver_ID = db.Column(db.INT(), nullable=False)
    customer_ID = db.Column(db.INT(), nullable=False)
    delivery_date = db.Column(db.DATE, nullable=False)
    timeslot = db.Column(db.VARCHAR(20), nullable=False)
    pickup_location = db.Column(db.VARCHAR(60), nullable=False)
    destination = db.Column(db.VARCHAR(60), nullable=False)
    delivery_item = db.Column(db.VARCHAR(40), nullable=False)
    description = db.Column(db.VARCHAR(120), nullable=False)
    payment_amount = db.Column(db.INT(), nullable=False)
    payment_status = db.Column(db.VARCHAR(6), nullable=False, default='Paid')
    receiver_name = db.Column(db.VARCHAR(64), nullable=False)
    delivery_status = db.Column(db.VARCHAR(10), nullable=False, default='New')
    created = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    last_updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    
    def __init__(self, delivery_ID, driver_ID, customer_ID, delivery_date, timeslot, pickup_location, destination, delivery_item, description, payment_amount, payment_status, receiver_name, delivery_status, created, last_updated):
        self.delivery_ID = delivery_ID
        self.driver_ID = driver_ID
        self.customer_ID = customer_ID
        self.delivery_date = delivery_date
        self.timeslot = timeslot
        self.pickup_location = pickup_location
        self.destination = destination
        self.delivery_item = delivery_item
        self.description = description
        self.payment_amount = payment_amount
        self.payment_status = payment_status
        self.receiver_name = receiver_name
        self.delivery_status = delivery_status
        self.created = created
        self.last_updated = last_updated

    def json(self):
        return {"delivery_ID": self.delivery_ID,
                "driver_ID": self.driver_ID, 
                "customer_ID": self.customer_ID,
                "delivery_date": self.delivery_date,
                "timeslot": self.timeslot, 
                "pickup_location": self.pickup_location, 
                "destination": self.destination,
                "delivery_item": self.delivery_item,
                "description": self.description,
                "payment_amount": self.payment_amount,
                "payment_status": self.payment_status,
                "receiver_name": self.receiver_name,
                "delivery_status": self.delivery_status,
                "created": self.created,
                "last_updated": self.last_updated
            }


#1. GET DELIVERY BY DELIVERY_ID (SPECIFIC)
@app.route("/delivery/<int:delivery_ID>")
def find_by_delivery_ID(delivery_ID):
    delivery = Delivery.query.filter_by(delivery_ID=delivery_ID).first()
    if delivery:
        return jsonify(
            {
                "code": 200,
                "data": delivery.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Delivery not found."
        }
    ), 404


#2. GET DELIVERY BY DRIVER_ID (DRIVER)
@app.route("/delivery/driver/<int:driver_ID>")
def find_by_driver_ID(driver_ID):
    deliverylist = Delivery.query.filter_by(driver_ID=driver_ID).all()
    if len(deliverylist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "deliveries": [delivery.json() for delivery in deliverylist]
                }
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no deliveries."
        }
    ), 404

    

#3. GET DELIVERY BY CUSTOMER_ID (CUSTOMER)
@app.route("/delivery/customer/<int:customer_ID>")
def find_by_customer_ID(customer_ID):
    deliverylist = Delivery.query.filter_by(customer_ID=customer_ID).all()
    print(deliverylist)
    if len(deliverylist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "deliveries": [delivery.json() for delivery in deliverylist]
                }
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no deliveries."
        }
    ), 404


# 4. CREATE NEW DELIVERY  
@app.route("/delivery", methods=['POST'])
def create_delivery():

    if request.is_json():
        data = request.get_json()
    else:
        return jsonify({
            'code': 501,
            'message': "Request not in json format."
        })

    #query from the last entry and increment by 1 for delivery_ID
    delivery = Delivery.query.order_by(Delivery.delivery_ID.desc()).first()
    if (delivery):
        delivery_ID = delivery.delivery_ID + 1
    else:
        delivery_ID = 1
    created = datetime.datetime.now()
    last_updated = created

    delivery = Delivery(delivery_ID=delivery_ID, **data, delivery_status="NEW", created=created, last_updated=last_updated)

    try:
        db.session.add(delivery)
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the delivery. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": delivery.json()
        }
    ), 201

# 5. UPDATE DELIVERY BY DELIVERY_ID
@app.route("/delivery/<int:delivery_ID>", methods=['PUT'])
def update_delivery(delivery_ID):
    try:
        delivery = Delivery.query.filter_by(delivery_ID=delivery_ID).first()

        if not delivery:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "delivery_ID": delivery_ID
                    },
                    "message": "Delivery not found."
                }
            ), 404

        data = request.get_json()
        if data['delivery_status']:
            delivery.delivery_status = data['delivery_status']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": delivery.json()
                }
            ), 200

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "delivery_ID": delivery_ID
                },
                "message": "An error occurred while updating the delivery. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
