from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os
from os import environ

app = Flask(__name__)
CORS(app)

HOST="0.0.0.0"
PORT = 5005

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/login'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/driver'
#there is a need for authentication to the database using root (user) and pass(if there is any)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Login(db.Model):
    __tablename__ = 'login'

    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(12), nullable=False)
    account_type = db.Column(db.String(8), nullable=False)
    ID = db.Column(db.Integer, nullable=False) 
    # customer_ID = db.Column(db.Integer, nullable=True)
    # driver_ID = db.Column(db.Integer, nullable=True)

    def __init__(self, username, password, account_type, ID):
        self.username = username
        self.password = password
        self.account_type = account_type
        self.ID = ID
        # self.customer_ID = customer_ID
        # self.driver_ID = driver_ID

    def json(self):
        return {
            "username": self.username, 
            "password": self.password, 
            "account_type": self.account_type, 
            "ID": self.ID
        }

#verify if a user exists
@app.route("/authenticate", methods=['POST'])
def authenticate_user():
    user_data = request.get_json()
    user_recorded = Login.query.filter_by(username=user_data['username']).first()
    if user_recorded:
        username = user_data['username']
        password = user_data['password']
        account_type = user_data['account_type']
        if username == user_recorded.username and password == user_recorded.password:
            if account_type=="customer":
                print("Authenticated! Welcome User " + username)
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "username":user_recorded.username,
                            "customer_ID": user_recorded.ID,
                            "account_type": "customer"
                        },
                        "message": "Login is successful"
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "username":user_recorded.username,
                            "driver_ID": user_recorded.ID,
                            "account_type": "driver"
                        },
                        "message": "Login is successful"
                    }
                )
    print("Unable to login, please sign up with Cheetah Express ;)")
    return jsonify(
        {
            "code": 404,
            "message": "User not found. Please sign up for an account with Cheetah Go ;)."
        }
    ), 404
    
#check if username is taken 
@app.route("/check_username_exist/<string:username>", methods=['GET'])
def check_username_exist(username):
    user_recorded = Login.query.filter_by(username=username).first()
    if (user_recorded):
        code = 400
        message = "The username is taken."
    else:
        code = 200
        message = "The username is available."
    return jsonify({
        "code": code,
        "username": user_recorded['username'],
        "message": message
        })

@app.route("/register_account/<string:username>", methods=['POST'])
def register_user(username):
    #POST request data
    # {
    #     "password": password,
    #     "account_type": account_type,
    #     "ID": ID
    # }

    data = request.get_json()
    account = Login(username, **data)
    try:
        db.session.add(account)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "username": username,
                    "account_type": data['account_type'],
                    "ID": data['ID']
                },
                "message": "An error occurred creating the account."
            }
        ), 500
    
    return jsonify(
        {
            "code": 201,
            'data': {
                "username": username,
                "account_type": data['account_type'],
                "ID": data['ID']
            }
        }
    ), 201


if __name__ =='__main__':
    print("This is flask " + os.path.basename(__file__) + " to enable users to log in ...")
    print(os.path.basename(__file__) + " is running on " + str(HOST) + ":" + str(PORT) + " ...")
    app.run(host=HOST, port=PORT, debug=True)