from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os
from os import environ

app = Flask(__name__)
CORS(app)

HOST = "0.0.0.0"
PORT = 5001


app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/driver'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/driver'
#there is a need for authentication to the database using root (user)x and pass(if there is any)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Driver(db.Model):
    __tablename__ = 'driver'

    driver_ID = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(64), nullable=False)
    driver_email = db.Column(db.String(128), nullable=False)
    driver_mobile = db.Column(db.Integer, nullable=False)
    driver_teleID = db.Column(db.String(20), nullable=True)
    vehicle_no = db.Column(db.String(8), nullable=False)

    def __init__(self, driver_ID, driver_name, driver_email, driver_mobile, driver_teleID, vehicle_no):
        self.driver_ID = driver_ID
        self.driver_name = driver_name
        self.driver_email = driver_email
        self.driver_mobile = driver_mobile
        self.driver_teleID = driver_teleID
        self.vehicle_no = vehicle_no

    def json(self):
        return {
            "driver_ID": self.driver_ID, 
            "driver_name": self.driver_name, 
            "driver_email": self.driver_email, 
            "driver_mobile": self.driver_mobile, 
            "driver_teleID": self.driver_teleID, 
            "vehicle_no": self.vehicle_no
        }

#return all drivers
@app.route("/driver")
def get_all():
    driver_list = Driver.query.all()
    if len(driver_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "drivers": [driver.json() for driver in driver_list]
                }
            }
        )
    return jsonify(
        {
            "code": 400,
            "message": "There are no drivers recorded."
        }
    ), 400

#return a specific driver
@app.route("/driver/<int:driver_ID>")
def find_by_driver_ID(driver_ID):
    driver = Driver.query.filter_by(driver_ID=driver_ID).first()
    if driver:
        return jsonify(
            {
                "code": 200,
                "data": driver.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Driver not found."
        }
    ), 404

#create a new driver
@app.route("/driver", methods=['POST'])
def create_driver():
    #create driver_ID, auto increment
    #if no driver in the database, the incoming driver have an id of 0
    recent_driver = Driver.query.order_by(Driver.driver_ID.desc()).first()
    if not (recent_driver):
        driver_ID = 0
    else:
        driver_ID = recent_driver.driver_ID + 1

    data = request.get_json()
    driver = Driver(driver_ID, **data)

    try:
        db.session.add(driver)
        db.session.commit()

    # if (Driver.query.filter_by(driver_ID=driver_ID).first()):
    #     return jsonify(
    #         {
    #             "code": 400,
    #             "data": {
    #                 "driver_ID": driver_ID
    #             },
    #             "message": "Driver already exists."
    #         }
    #     ), 400
    
    # data = request.get_json()
    # driver = Driver(driver_ID, **data)

    # try:
    #     db.session.add(driver)
    #     db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "driver_ID": driver_ID
                },
                "message": "An error occurred creating the driver."
            }
        ), 500
    
    return jsonify(
        {
            "code": 201,
            'data': driver.json()
        }
    ), 201

#delete a driver
@app.route("/driver/<int:driver_ID>", methods=['DELETE'])
def delete_driver(driver_ID):
    driver = Driver.query.filter_by(driver_ID=driver_ID).first()
    if not (driver):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "driver_ID": driver_ID
                },
                "message": "This driver does not exist."
            }
        ), 400

    try:
        db.session.delete(driver)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "driver_ID": driver_ID
                },
                "message": "An error occurred creating the driver."
            }
        ), 500
    
    return jsonify(
        {
            "code": 203,
            'data': driver.json(),
            "message": "Driver has successfully been deleted."
        }
    ), 203

#update a driver 
@app.route("/driver/<int:driver_ID>", methods=['PUT'])
def update_driver(driver_ID):
    old_driver = Driver.query.filter_by(driver_ID=driver_ID).first()
    if not (old_driver):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "driver_ID": driver_ID
                },
                "message": "Driver does not exist."
            }
        ), 400

    # data = request.get_json()
    # new_driver = Driver(driver_ID, **data)
    new_driver = request.get_json()

    try:
        # old_driver.DName = new_driver.DName
        # old_driver.DEmail = new_driver.DEmail
        # old_driver.DMobile = new_driver.DMobile
        # old_driver.DTeleID = new_driver.DTeleID
        # old_driver.vehicle_no = new_driver.vehicle_no

        old_driver.DName = new_driver['DName']
        old_driver.DEmail = new_driver['DEmail']
        old_driver.DMobile = new_driver['DMobile']
        old_driver.DTeleID = new_driver['DTeleID']
        old_driver.vehicle_no = new_driver['vehicle_no']
        db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "driver_ID": driver_ID
                },
                "message": "An error occurred updating the driver."
            }
        ), 500
    
    return jsonify(
        {
            "code": 202,
            'data': old_driver.json(),
            "message": "Driver has successfully been updated."
        }
    ), 202


if __name__ =='__main__':
    print("This is flask " + os.path.basename(__file__) + " for Driver details...")
    print(os.path.basename(__file__) + " is running on " + str(HOST) + ":" + str(PORT) + " ...")
    app.run(host=HOST, port=PORT, debug=True)
