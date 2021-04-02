#COMPLEX: DRIVER COMPLETES A JOB 
# DRIVER UPDATES DELIVERY STATUS: COMPLETION 
# NOTIFY DRIVERS AND CUSTOMERS OF COMPLETED DELIVERY 

#TRIGGER FOR THIS EVENT: WHEN DRIVER ARRIVES AT THE DOOR, HE WILL PRESS BUTTON ON UI 
#THIS BUTTON WILL INVOKE THE COMPLEX MICROSERVICE AND UPDATE STATUS 

from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

error_URL = "http:localhost:5007/error"

# Main function that calls other functions
@app.route("/complete_delivery/<int:delivery_ID>", methods=['POST'])
def complete_delivery(delivery_ID):

    #Check if input format and data of request are JSON 
    if request.is_json:
        try:
            delivery = request.get_json()
            print("\nThe following delivery is complete:", delivery)

            #invokes update_delivery_status function
            #delivery = {'status': 'completed!'}
            #delivery_ID = 1
            result = update_delivery_status(delivery, delivery_ID)
            return jsonify(result), 200

        # Unexpected error in code
        except Exception as e:
            return jsonify({
                "code": 500,
                "message": "oh no ,delivery_complete.py internal error"
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
    delivery_result = invoke_http("http://localhost:5000/delivery/" + str(delivery_ID), method='PUT', json=delivery)
    print('delivery_result:', delivery_result)
    #{'code': 500, 'message': 'Invalid JSON output from service: http://localhost:5000/delivery/1. Expecting value: line 1 column 1 (char 0)'}

    # 3. Check the delivery result; if a failure, send it to the error microservice.
    code = delivery_result["code"]
    message = json.dumps(delivery_result)

    #if code result is not good 
    if code not in range(200, 300):

        print('\n\n-----Publishing the (delivery error) message with routing_key=delivery.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="delivery.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        print("\nDelivery status ({:d}) published to the RabbitMQ Exchange:".format(
            code), delivery_result)

        # 5. Return error 
        return {
            "code": 500,
            "data": {"delivery_result": delivery_result},
            "message": "Delivery update failure, sent for error handling."
        }

        #6. Invoke Notification AMQP
    message = "Delivery Completed!"
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="customer.completed.order", body=message)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="driver.completed.order", body=message)
    
    #if notification got error: assume no error 

    # 6. Return updated delivery, notification status 
    return {
        "code": 201,
        "data": {
            "order_result": delivery_result
            # "notification_result": notification_result
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.



#old notification microservice
    # 6. Invoke Notification microservice (TBC)
    # print('\n\n-----Invoking notification microservice-----')
    # notification_result = invoke_http(
    #     "http://localhost:5008/notification", method="POST", json=delivery_result['data'])
    # print("notification_result:", notification_result, '\n')

    # Check the notification result;
    # if a failure, send it to the error microservice.
    # code = notification_result["code"]
    # if code not in range(200, 300):

    # Inform the error microservice
        # print('\n\n-----Invoking error microservice as notification fails-----')
        # invoke_http("http:localhost:5007/error", method="POST", json=notification_result)
        # print("Notification status ({:d}) sent to the error microservice:".format(
        #     code), notification_result)

    # 7. Return error
        # return {
        #     "code": 400,
        #     "data": {
        #         "delivery_result": delivery_result,
        #         "Notification_result": notification_result
        #     },
        #     "message": "Error when sending notification to driver/customer."
        # }