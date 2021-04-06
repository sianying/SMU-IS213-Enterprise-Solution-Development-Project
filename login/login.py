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

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/login'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/driver'
#there is a need for authentication to the database using root (user) and pass(if there is any)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Login(db.Model):
    __tablename__ = 'login'

    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(12), nullable=False)
    account_type = db.Column(db.String(8), nullable=False)
    customer_ID = db.Column(db.Integer, nullable=True) 
    driver_ID = db.Column(db.Integer, nullable=True) 
    # customer_ID = db.Column(db.Integer, nullable=True)
    # driver_ID = db.Column(db.Integer, nullable=True)

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

#verify if a user exists
@app.route("/authenticate", methods=['POST'])
def authenticate_user():
    user_data = request.get_json()
    user_recorded = Login.query.filter_by(username=user_data['username']).first()
    account_type = user_recorded.account_type
    #eg. customer_ID or driver_ID
    user_ID_header = account_type + "_ID"
    user_ID = user_recorded.user_ID_header
    if user_recorded:
        username = user_data['username']
        password = user_data['password']
        account_type = user_data['account_type']

        hashed = user_recorded['password']
        # if username == user_recorded.username and password == user_recorded.password:
        if username == user_recorded.username and bcrypt.checkpw(password, hashed):
            print("Authenticated! Welcome User " + username)
            return jsonify({
                    "code": 200,
                    "data": {
                        "username":user_recorded.username,
                        user_ID_header: user_recorded.user_ID,
                        "account_type": account_type
                    },
                    "message": "Login is successful"
                })
    print("Unable to login, please sign up with Cheetah Express ;)")
    return jsonify({
            "code": 404,
            "message": "User not found. Please sign up for an account with Cheetah Go ;)."
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
    #POST request data
    # {
    #     "password": password,
    #     "account_type": account_type,
    #     "customer_ID": customer_ID or "driver_ID": driver_ID
    # }

    #verifies if the user exists, but this is covered in covered in the other function
    # user_recorded = Login.query.filter_by(username=username).first()
    # if user_recorded:
    #     account_type = user_recorded.account_type
    #     if account_type == "customer":
    #         return jsonify({
    #             "code": 400,
    #             "data": {
    #                 "username": user_recorded.username,
    #                 "account_type": user_recorded.account_type,
    #                 "customer_ID": user_recorded.customer_ID
    #             },
    #             "message": "User already exists. Please choose another username."
    #         }), 400
    #     else:
    #         return jsonify({
    #             "code": 400,
    #             "data": {
    #                 "username": user_recorded.username,
    #                 "account_type": user_recorded.account_type,
    #                 "driver_ID": user_recorded.driver_ID
    #             },
    #             "message": "User already exists. Please choose another username."
    #             }), 400

    data = request.get_json()
    account_type = data['account_type']
    user_ID_header = account_type  + "_ID"

    account = Login(username, **data)
    try:
        db.session.add(account)
        db.session.commit()
    except:
        return jsonify({
                "code": 500,
                "data": {
                    "username": username,
                    "account_type": account_type,
                    user_ID_header: data[user_ID_header]
                },
                "message": "An error occurred creating the account."
            }), 500
    
    return jsonify(
        {
            "code": 201,
            'data': {
                "username": username,
                "account_type": account_type,
                user_ID_header: data[user_ID_header]
            }
        }
    ), 201

def create_hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)

    return hashed



if __name__ =='__main__':
    print("This is flask " + os.path.basename(__file__) + " to enable users to log in ...")
    print(os.path.basename(__file__) + " is running on " + str(HOST) + ":" + str(PORT) + " ...")
    app.run(host=HOST, port=PORT, debug=True)