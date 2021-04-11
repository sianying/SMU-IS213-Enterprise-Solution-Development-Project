from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ
import datetime

import requests
from invokes import invoke_http
import amqp_setup

import pika
import json

HOST = "0.0.0.0"
PORT = 5105

app = Flask(__name__)
CORS(app)

############################################################################################################
#User Registration
#1. depending on the role of the user, check if the user already has an account (customer or driver) using Login Microservice
#2. once verified that the account do not exists, register user particulars using Customer or Driver Microservice
#3. register users using Login Microservice (create new account)
##############################################################################################################

login_URL = environ.get('loginURL') or "http://127.0.0.1:5005"
driver_URL = environ.get('driverURL') or "http://127.0.0.1:5001/driver"
customer_URL = environ.get('customerURL') or "http://127.0.0.1:5002/customer"
schedule_URL = environ.get('scheduleURL') or "http://127.0.0.1:5004/schedule"

# POST request format in the URL: "username": username,
# {
#     "password": password,
#     "name": name,
#     "email": email,
#     "teleID": teleID,
#     "mobile": mobile
#     "vehicle_no": vehicle_no     #this only applies to driver#
#     "account_type": account_type

# }

@app.route("/register_user/<string:username>", methods=['POST'])
def register_user(username):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            data = request.get_json()
            print("\nReceived an data in JSON:", data)

            #1. Invoke Login MS to check if username is taken
            # Invoke the Login Microservice (/check_username_exist)
            print('\n-----Invoking Login microservice-----')
            username_data = invoke_http(login_URL + "/" + "check_username_exist" + "/" + username, method='GET')
            # print('payment_results:'+ str(username_data) + "\n")

            code = username_data["code"]
            if code not in range(200, 300):
                error_message = {
                    "code": 501,
                    "data": {"username_data": username_data},
                    "message": "Failed to retrieve the user's account using Login Microservice (GET), sent for error handling."
                    }
                print('\n\n-----Publishing the (login error) message with routing_key=login.error-----')
                message=json.dumps(error_message)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="login.error", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))

            #code 200 means username not taken
            #code 400 means bad request username is taken
            code= username_data['code']
            if code == 400:
                return jsonify({
                    username_data
                })
            
            #2. Register user depending on their account_type {processRegisterCustomer, processRegisterDriver}
            # use the returned customer_ID or driver_ID to create the entry in Login Microservice
            account_type = data['account_type']
            if account_type == "customer":
                user_ID = registerCustomer(data)
            else:
                user_ID = registerDriver(data)

            #3. Register user using Login Microservice (POST request)
            # do the actual work {processRegisterUser}
            password = data['password']
            register_user = registerUserAccount(username, user_ID, password, account_type)


            # print(register_user)
            return register_user
            # print('\n------------------------')
            # print('\nresult: ', result)
            # return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "register_user.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def registerCustomer(data):
    #restructure customer POST request data for Customer Microservice
    customer_data = {
        "customer_name": data['name'],
        "customer_email": data['email'], 
        "customer_mobile": data['mobile'], 
        "customer_teleID": data['teleID']
    }
    # print(customer_data)
    # print(type(customer_data))
    # Invoke the Customer Microservice (/customer)
    print('\n-----Invoking Customer microservice-----')
    customer_data = invoke_http(customer_URL, method='POST', json=customer_data)
    # print('customer_results:' + str(customer_data) + "\n")

    code = customer_data["code"]
    if code not in range(200, 300):
        error_message = {
                "code": 501,
                "data": {"customer_data": customer_data},
                "message": "Failed to create customer profile using Customer MS, sent for error handling."
            }
        print('\n\n-----Publishing the (login error) message with routing_key=login.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="login.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
        return error_message
    
    #return customer_ID
    customer_ID = customer_data['data']['customer_ID']
    return customer_ID
    

def registerDriver(data):
    #restructure driver POST request data for driver Microservice
    driver_data = {
        "driver_name": data['name'],
        "driver_email": data['email'], 
        "driver_mobile": data['mobile'], 
        "driver_teleID": data['teleID'],
        "vehicle_no": data['vehicle_no']
    }
    # Invoke the driver Microservice (/driver)
    print('\n-----Invoking Driver microservice-----')
    driver_data = invoke_http(driver_URL, method='POST', json=driver_data)
    # print('driver_results:' + str(driver_data) + "\n")

    code = driver_data["code"]
    if code not in range(200, 300):
        error_message = {
                "code": 501,
                "data": {"driver_data": driver_data},
                "message": "Failed to create driver profile using Driver Microservice (POST), sent for error handling."
            }
        print('\n\n-----Publishing the (driver error) message with routing_key=driver.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="driver.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
        return error_message
        
    driver_ID = driver_data['data']['driver_ID']
    # return driver_ID

    #getting the date to create a new empty schedule for the driver
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    schedule_data = {
        "driver_ID": driver_ID,
        "delivery_date": today_date,
        "t_8_to_10": False,
        "t_10_to_12": False,
        "t_12_to_2": False,
        "t_2_to_4": False,
        "t_4_to_6": False
    }
    #Invoke the Schedule Microservice to create a schedule for the driver
    print('\n-----Invoking Schedule microservice-----')
    driver_schedule = invoke_http(schedule_URL, method='POST', json=schedule_data)
    print('driver_schedule:' + str(driver_schedule) + "\n")

    #error handling
    code = driver_data["code"]
    if code not in range(200, 300):
        error_message = {
                "code": 501,
                "data": {"driver_schedule": driver_schedule},
                "message": "Failed to create driver profile using Driver Microservice (POST), sent for error handling."
            }
        print('\n\n-----Publishing the (driver error) message with routing_key=driver.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="driver.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
        return error_message

    return driver_ID


def registerUserAccount(username, user_ID, password, account_type):
    #1. Restructure the data for Login Microservice account registration (POST)
    if account_type == "customer":
        account_data = {
            "password": password,
            "account_type": "customer",
            "customer_ID": user_ID,
            "driver_ID": "NULL"
        }
    else:
        account_data = {
            "password": password,
            "account_type": "driver",
            "driver_ID": user_ID,
            "customer_ID": "NULL"
        }

    # 2. Invoke Login MS to register user 
    # Invoke the Login Microservice (/register_account/<string: username>)
    print('\n-----Invoking Login microservice-----')
    account_registered = invoke_http(login_URL + "/register_account/" + str(username), method='POST', json=account_data)
    print('account_results:' + str(account_registered) + "\n")

    #error handling
    code = account_registered['code']
    if code not in range(200, 300):
        error_message = {
            "code": 501,
            "data": {"account_registered": account_registered},
            "message": "Failed to register user using the Login Microservice (POST), sent for error handling."
        }
        print('\n\n-----Publishing the (login error) message with routing_key=login.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="login.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
        return error_message

    return account_registered

    #data format that is being returned
    # {
    #     "code": 201,
    #     'data': {
    #         "username": username,
    #         "account_type": data['account_type'],
    #         "ID": data['ID']
    #     }
    # }


# def send_notification(order_ID):
#     #invoke the notification AMQP to inform customer of new delivery order
#     print('\n\n-----Invoking customer_notification microservice-----')
#     print('\n\n-----Publishing the (successful order creation) message with routing_key=customer.order.created-----')  
#     message_customer = "Your order has been created. Your order ID is", order_ID, "Thank you for using Cheetah Express! "
#     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="customer.order.created", 
#             body=message_customer)

#     #invoke the notification AMQP to inform driver of new delivery order
#     print('\n\n-----Invoking driver_notification microservice-----')
#     print('\n\n-----Publishing the (successful order creation) message with routing_key=driver.order.created-----')  
#     message_driver = "You have a new delivery order! The order ID is", order_ID
#     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="driver.order.created", 
#             body=message_customer)

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for registering a user...")
    print("Running on port: " + str(PORT) + " ...")
    app.run(host=HOST, port=PORT, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
