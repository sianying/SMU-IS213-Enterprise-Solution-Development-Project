from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/delivery_db'
#'mysql+mysqlconnector://root@localhost:3306/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
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
    #wa idk how to include for the timestamps and default values help
    status = db.Column(db.VARCHAR(10), nullable=False, default='New')
    created = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    last_updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    #default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    
    def __init__(self, delivery_ID, driver_ID, customer_ID, delivery_date, timeslot, pickup_location, destination, status, created, last_updated):
        self.delivery_ID = delivery_ID
        self.driver_ID = driver_ID
        self.customer_ID = customer_ID
        self.delivery_date = delivery_date
        self.timeslot = timeslot
        self.pickup_location = pickup_location
        self.destination = destination
        self.status = status
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
                "status": self.status,
                "created": self.created,
                "last_updated": self.last_updated
            }

#dont really have a scenario where we will get all deliveries but i guess its a useful function to have
# 1. GET ALL DELIVERIES 
@app.route("/delivery")
def get_all():
    deliverylist = Delivery.query.all()
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

#to query a specific delivery
#2. GET DELIVERY BY DELIVERY_ID (SPECIFIC)
@app.route("/delivery/<int:delivery_ID>")
def find_by_delivery_ID(delivery_ID):
    delivery = Delivery.query.filter_by(delivery_ID=delivery_ID).first()
    if delivery:
        return jsonify(
            {
                "code": 200,
                #filter columns accord to what driver shud see
                "data": delivery.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Delivery not found."
        }
    ), 404

#for drivers to see their deliveries 
#3. GET DELIVERY BY DRIVER_ID (DRIVER)
@app.route("/delivery/driver/<int:driver_ID>")
def find_by_driver_ID(driver_ID):
    delivery = Delivery.query.filter_by(driver_ID=driver_ID).first()
    if delivery:
        delivery = delivery.json()
        return jsonify(
            {
                "code": 200,
                #filter columns accord to what driver shud see
                "data": delivery['pickup_location'],
                "data1": delivery['timeslot']
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Delivery not found."
        }
    ), 404

#for customers to see their deliveries
#4. GET DELIVERY BY CUSTOMER_ID (CUSTOMER)
@app.route("/delivery/customer/<int:customer_ID>")
def find_by_customer_ID(customer_ID):
    delivery = Delivery.query.filter_by(customer_ID=customer_ID).first()
    if delivery:
        return jsonify(
            {
                "code": 200,
                #filter columns accord to what customer shud see
                "data": delivery.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Delivery not found."
        }
    ), 404


# 5. CREATE NEW DELIVERY  
@app.route("/delivery", methods=['POST'])
def create_delivery():
    #diagram might need to change, necessary to find an available driver first and add it into the request
    driver_ID=request.json.get('driver_ID', None)
    customer_ID = request.json.get('customer_ID', None)
    delivery_date = request.json.get('delivery_date', None)
    timeslot = request.json.get('timeslot', None)
    pickup_location = request.json.get('pickup_location', None)
    destination = request.json.get('destination', None)

    delivery = Delivery.query.order_by(Delivery.delivery_ID.desc()).first()
    delivery_ID= delivery.delivery_ID + 1

    created=datetime.datetime.now()
    last_updated=created

    delivery=Delivery(delivery_ID=delivery_ID, driver_ID= driver_ID, customer_ID=customer_ID, delivery_date=delivery_date, timeslot=timeslot, pickup_location=pickup_location, destination=destination, status='NEW', created=created, last_updated=last_updated) 

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

# 6. UPDATE DELIVERY BY DELIVERY_ID (DRIVER), status can be completion or smth else
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

        # update status and timestamp
        data = request.get_json()
        if data['status']:
            #i feel like need update timestamp also, but idk whether it's automatic
            #they didnt update timestamp in the simple order microservice
            delivery.status = data['status']
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

#7. Delete deliveries (IN CASE OF CANCELLED DELIVERIES)
@app.route("/delivery/<int:delivery_ID>", methods=['DELETE'])
def delete_delivery(delivery_ID):
    delivery = Delivery.query.filter_by(delivery_ID=delivery_ID).first()
    if not (delivery):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "delivery_ID": delivery_ID
                },
                "message": "This delivery does not exist."
            }
        ), 400

    try:
        db.session.delete(delivery)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "delivery_ID": delivery_ID
                },
                "message": "An error occurred deleting the delivery."
            }
        ), 500
    
    return jsonify(
        {
            "code": 203,
            'data': delivery.json(),
            "message": "Delivery has successfully been deleted."
        }
    ), 203

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
