from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/driver'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/driver'
#there is a need for authentication to the database using root (user) and pass(if there is any)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Driver(db.Model):
    __tablename__ = 'driver'

    DID = db.Column(db.Integer, primary_key=True)
    DName = db.Column(db.String(64), nullable=False)
    DEmail = db.Column(db.String(128), nullable=False)
    DMobile = db.Column(db.Integer, nullable=False)
    DTeleID = db.Column(db.String(20), nullable=True)
    vehicle_no = db.Column(db.String(8), nullable=False)

    def __init__(self, DID, DName, DEmail, DMobile, DTeleID, vehicle_no):
        self.DID = DID
        self.DName = DName
        self.DEmail = DEmail
        self.DMobile = DMobile
        self.DTeleID = DTeleID
        self.vehicle_no = vehicle_no

    def json(self):
        return {
            "DID": self.DID, 
            "DName": self.DName, 
            "DEmail": self.DEmail, 
            "DMobile": self.DMobile, 
            "DTeleID": self.DTeleID, 
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
@app.route("/driver/<int:DID>")
def find_by_DID(DID):
    driver = Driver.query.filter_by(DID=DID).first()
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
@app.route("/driver/<int:DID>", methods=['POST'])
def create_driver(DID):
    if (Driver.query.filter_by(DID=DID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "DID": DID
                },
                "message": "Driver already exists."
            }
        ), 400
    
    data = request.get_json()
    driver = Driver(DID, **data)

    try:
        db.session.add(driver)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "DID": DID
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
@app.route("/driver/<int:DID>", methods=['DELETE'])
def delete_driver(DID):
    driver = Driver.query.filter_by(DID=DID).first()
    if not (driver):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "DID": DID
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
                    "DID": DID
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
@app.route("/driver/<int:DID>", methods=['PUT'])
def update_driver(DID):
    old_driver = Driver.query.filter_by(DID=DID).first()
    if not (old_driver):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "DID": DID
                },
                "message": "Driver does not exist."
            }
        ), 400

    data = request.get_json()
    new_driver = Driver(DID, **data)

    try:
        old_driver.DName = new_driver.DName
        old_driver.DEmail = new_driver.DEmail
        old_driver.DMobile = new_driver.DMobile
        old_driver.DTeleID = new_driver.DTeleID
        old_driver.vehicle_no = new_driver.vehicle_no
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "DID": DID
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
    app.run(port=5000, debug=True)