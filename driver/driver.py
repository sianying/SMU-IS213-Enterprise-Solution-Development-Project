from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os
from os import environ

app = Flask(__name__)
CORS(app)

HOST = "0.0.0.0"
PORT = 5001

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@127.0.0.1:3306/driver'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Driver(db.Model):
    __tablename__ = 'driver'

    driver_ID = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(64), nullable=False)
    driver_email = db.Column(db.String(128), nullable=False)
    driver_mobile = db.Column(db.Integer, nullable=False)
    driver_teleID = db.Column(db.String(20), nullable=True)
    vehicle_no = db.Column(db.String(8), nullable=False)
    tele_chat_ID = db.Column(db.String(15), nullable=True)

    def __init__(self, driver_ID, driver_name, driver_email, driver_mobile, driver_teleID, vehicle_no, tele_chat_ID):
        self.driver_ID = driver_ID
        self.driver_name = driver_name
        self.driver_email = driver_email
        self.driver_mobile = driver_mobile
        self.driver_teleID = driver_teleID
        self.vehicle_no = vehicle_no
        self.tele_chat_ID = tele_chat_ID


    def json(self):
        return {
            "driver_ID": self.driver_ID, 
            "driver_name": self.driver_name, 
            "driver_email": self.driver_email, 
            "driver_mobile": self.driver_mobile, 
            "driver_teleID": self.driver_teleID, 
            "vehicle_no": self.vehicle_no,
            "tele_chat_ID": self.tele_chat_ID
        }

# 1. return all drivers
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

# 2. return a specific driver
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

# 3. create a new driver
@app.route("/driver", methods=['POST'])
def create_driver():
    #create driver_ID, auto increment
    #if no driver in the database, the incoming driver have an id of 0
    recent_driver = Driver.query.order_by(Driver.driver_ID.desc()).first()
    if (recent_driver):
        driver_ID = recent_driver.driver_ID + 1
    else:
        driver_ID = 1

    data = request.get_json()
    driver = Driver(driver_ID, **data)

    try:
        db.session.add(driver)
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
            "code": 201,
            'data': driver.json()
        }
    ), 201

# 4. Update driver (chat_id), teleID is also a unique identifier 
@app.route("/driver/<string:driver_teleID>", methods=['PUT'])
def update_driver_chatID(driver_teleID):
    driver = Driver.query.filter_by(driver_teleID=driver_teleID).first()
    if not (driver):
        return jsonify({
                "code": 404,
                "data": {
                    "driver_teleID": driver_teleID
                },
                "message": "Driver does not exist."
            }), 404

    data = request.get_json()
    #chat_ID is stored as varchar/string in db, hence, convert the incoming to str for comparison
    input_tele_chat_ID = str(data['tele_chat_ID'])

    if driver.tele_chat_ID == input_tele_chat_ID:
        return jsonify({
            "code": 400,
                "data": {
                    "driver_teleID": driver_teleID
                },
            "message": "Driver has already registered his chat_ID."
        }), 400

    try:
        driver.tele_chat_ID = input_tele_chat_ID
        db.session.commit()

    except:
        return jsonify({
                "code": 500,
                "data": {
                    "driver_teleID": driver_teleID
                },
                "message": "An error occurred updating the driver."
            }), 500
    
    return jsonify({
            "code": 202,
            'data': driver.json(),
            "message": "Driver chat_ID has successfully been updated."
        }), 202

if __name__ =='__main__':
    print("This is flask " + os.path.basename(__file__) + " for Driver details...")
    print(os.path.basename(__file__) + " is running on " + str(HOST) + ":" + str(PORT) + " ...")
    app.run(host=HOST, port=PORT, debug=True)
