#COMPLEX: DRIVER COMPLETES A JOB 
# DRIVER UPDATES DELIVERY STATUS: COMPLETION 
# NOTIFY DRIVERS AND CUSTOMERS OF COMPLETED DELIVERY 

#TRIGGER FOR THIS EVENT: WHEN DRIVER ARRIVES AT THE DOOR, HE WILL PRESS BUTTON ON UI 
#THIS BUTTON WILL INVOKE THE COMPLEX MICROSERVICE AND UPDATE STATUS 

from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
from os import environ
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

HOST = "0.0.0.0"
PORT = 5103

deliveryURL=environ.get('deliveryURL') or 'http://127.0.0.1:5000/delivery'
driverURL= environ.get('driverURL') or 'http://127.0.0.1:5001/driver'
customerURL= environ.get('customerURL') or 'http://127.0.0.1:5002/customer'

# Main function that calls other functions
@app.route("/complete_delivery/<int:delivery_ID>", methods=['POST'])
def complete_delivery(delivery_ID):

    #Check if input format and data of request are JSON 
    if request.is_json:
        try:
            delivery = request.get_json()
            result = update_delivery_status(delivery, delivery_ID)
            return jsonify(result), 200

        # Unexpected error in code
        except Exception as e:
            return jsonify({
                "code": 500,
                "message": "delivery_complete.py internal error"
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# Update and return new delivery status (delivery MS)
def update_delivery_status(delivery, delivery_ID):

    # 2. Invoke the delivery microservice
    print('\n-----Invoking delivery microservice-----')
    delivery_result = invoke_http(deliveryURL + '/' + str(delivery_ID), method='PUT', json=delivery)
    
    # 3. Check the delivery result; if a failure, send it to the error microservice.
    code = delivery_result['code']
    if code not in range(200, 300):
        error_message = {
            "code": 501,
            "data": {"delivery_result": delivery_result},
            "message": "Failed to retrieve delivery data, sent for error handling."
        }
        print('\n\n-----Publishing the (delivery error) message with routing_key=DriverCompleteDelivery.delivery.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="DriverCompleteDelivery.delivery.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nDelivery MS call status ({:d}) published to the RabbitMQ Exchange:".format(code), delivery_result)
        return error_message

    # 5. invoke the driver microservice
    driver_ID = delivery_result['data']['driver_ID']
    print('\n-----Invoking driver microservice-----')
    driver_result = invoke_http(driverURL + '/' + str(driver_ID), method='GET')

    # 6. Check the driver result; if a failure, send it to the error microservice.
    code = driver_result["code"]
    if code not in range(200, 300):
        error_message = {
            "code": 502,
            "data": {"driver_result": driver_result},
            "message": "Failed to retrieve driver data (GET), sent for error handling."
        }
        print('\n\n-----Publishing the (driver error) message with routing_key=DriverCompleteDelivery.driver.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="DriverCompleteDelivery.driver.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nDriver MS call status ({:d}) published to the RabbitMQ Exchange:".format(code), driver_result)
        return error_message


    delivery_driver = driver_result['data']['driver_name'] 
    driver_tele_chat_ID = driver_result['data']['tele_chat_ID']

    customer_ID = delivery_result['data']['customer_ID']
    #7. Invoke customer to retrieve the customer tele_chat_ID
    print('\n-----Invoking customer microservice-----')
    customer_data = invoke_http(customerURL + "/" + str(customer_ID), method='GET')
    if code not in range(200, 300):
        error_message = {
            "code": 502,
            "data": {"customer_data": customer_data},
            "message": "Failed to retrieve customer data, sent for error handling."
        }
        print('\n\n-----Publishing the (customer error) message with routing_key=DriverCompleteDelivery.customer.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="DriverCompleteDelivery.customer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nCustomer MS call status ({:d}) published to the RabbitMQ Exchange:".format(code), customer_data)
        return error_message
        
    customer_tele_chat_ID = customer_data['data']['tele_chat_ID']

    #6. Invoke Customer Notification AMQP
    message = "Delivery Completed! \n\n" + "Delivery Order ID: " + str(delivery_result['data']['delivery_ID']) + " was delivered by " + str(delivery_driver) + " to " + str(delivery_result['data']['receiver_name']) + " on " + str(delivery_result['data']['last_updated'])
    messages = json.dumps({
            "customer_message": message,
            "customer_tele_chat_ID": customer_tele_chat_ID,
            "driver_message": message,
            "driver_tele_chat_ID": driver_tele_chat_ID 
        })

    print('\n\n-----Publishing the (customer & driver) message with routing_key=customer.CompleteDelivery and routing_key=driver.CompleteDelivery-----')
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="customer.CompleteDelivery", body=messages)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="driver.CompleteDelivery", body=messages)
    
    # 6. Return updated delivery, notification status 
    return {
        "code": 201,
        "data": {
            "order_result": delivery_result
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
        " for placing an order...")
    app.run(host=HOST, port=PORT, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.


