from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os
from os import environ

import bcrypt

app = Flask(__name__)
CORS(app)

HOST="0.0.0.0"
PORT = 5005

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@127.0.0.1:3306/login'
#there is a need for authentication to the database using root (user) and pass(if there is any)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Login(db.Model):
    __tablename__ = 'login'

    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    account_type = db.Column(db.String(8), nullable=False)
    customer_ID = db.Column(db.Integer, nullable=True, default=None) 
    driver_ID = db.Column(db.Integer, nullable=True, default=None) 

    def __init__(self, username, password, account_type, customer_ID, driver_ID):
        self.username = username
        self.password = password
        self.account_type = account_type
        self.customer_ID = customer_ID
        self.driver_ID = driver_ID

    def json(self):
        return {
            "username": self.username, 
            "password": self.password, 
            "account_type": self.account_type, 
            "customer_ID": self.customer_ID,
            "driver_ID": self.driver_ID
        }

#verify if a user exists & authenticate
@app.route("/authenticate", methods=['POST'])
def authenticate_user():
    user_data = request.get_json()
    user_recorded = Login.query.filter_by(username=user_data['username']).first()
    account_type = user_recorded.account_type

    if user_recorded is not None:
        account_type = user_data['account_type']
        username = user_data['username']
        password = user_data['password']
        hashed = user_recorded.password

        #encode the plain text password to match the hashed password
        encode_password = password.encode('utf-8')
        encode_hashed = hashed.encode('utf-8')
        if username == user_recorded.username and bcrypt.checkpw(encode_password, encode_hashed):
            if account_type == "customer":
                return jsonify({
                        "code": 200,
                        "data": {
                            "username": user_recorded.username,
                            "customer_ID": user_recorded.customer_ID,
                            "account_type": account_type
                        },
                        "message": "Login is successful"
                    })
            else:
                return jsonify({
                        "code": 200,
                        "data": {
                            "username":user_recorded.username,
                            "driver_ID": user_recorded.driver_ID,
                            "account_type": account_type
                        },
                        "message": "Login is successful"
                    })
    return jsonify({
            "code": 404,
            "message": "User not found. Please sign up for an account with Cheetah Express."
        }), 404
    
#check if username is taken 
@app.route("/check_username_exist/<string:username>", methods=['GET'])
def check_username_exist(username):
    user_recorded = Login.query.filter_by(username=username).first()
    if (user_recorded):
        return jsonify({
            "code": 400,
            "username": username,
            "message": "The username is taken :("
        }), 400
    else:
        return jsonify({
            "code": 200,
            "username": username,
            "message": "The username is available."
        }), 200


#creates user
@app.route("/register_account/<string:username>", methods=['POST'])
def register_user(username):

    data = request.get_json()
    account_type = data['account_type']
    password = data['password']
    encoded_password = password.encode('utf-8')
    hashed = create_hash_password(encoded_password)
    #decode hashed password for db storage
    decode_hashed = hashed.decode('utf-8')
    #reconstruct the data for the db addition
    if account_type == "customer":
        customer_ID = data['customer_ID']
        account = Login(username, decode_hashed, account_type, customer_ID, None)
    else:
        driver_ID = data['driver_ID']
        account = Login(username, decode_hashed, account_type, None, driver_ID)

    try:
        db.session.add(account)
        db.session.commit()
    except ValueError as e:
        if account_type == "customer":
            return jsonify({
                    "code": 500,
                    "data": {
                        "username": username,
                        "account_type": account_type,
                        "customer_ID": customer_ID
                    },
                    "message": "An error occurred creating the account."
                }), 500
        else:
            return jsonify({
                    "code": 500,
                    "data": {
                        "username": username,
                        "account_type": account_type,
                        "driver_ID": driver_ID
                    },
                    "message": "An error occurred creating the account."
                }), 500
    
    if account_type == "customer":
        return jsonify({
            "code": 201,
            'data': {
                "username": username,
                "account_type": account_type,
                "customer_ID": customer_ID
            }
        }), 201
    else:
        return jsonify({
            "code": 201,
            'data': {
                "username": username,
                "account_type": account_type,
                "driver_ID": driver_ID
            }
        }), 201

def create_hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed



if __name__ =='__main__':
    print("This is flask " + os.path.basename(__file__) + " to enable users to log in ...")
    print(os.path.basename(__file__) + " is running on " + str(HOST) + ":" + str(PORT) + " ...")
    app.run(host=HOST, port=PORT, debug=True)
