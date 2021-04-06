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

    delivery_result = invoke_http("http://localhost:5000/delivery/" + str(delivery_ID), method='PUT', json=delivery)
    
    # 3. Check the delivery result; if a failure, send it to the error microservice.
    code = delivery_result["code"]
    if code not in range(200, 300):
        print('\n\n-----Publishing the (delivery error) message with routing_key=DriverCompleteDelivery.delivery.error-----')
        message=json.dumps(delivery_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="DriverCompleteDelivery.delivery.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nDelivery MS call status ({:d}) published to the RabbitMQ Exchange:".format(code), delivery_result)

        return {
            "code": 501,
            "data": {"delivery_result": delivery_result},
            "message": "Failed to retrieve delivery data, sent for error handling."
        }

    # 5. invoke the driver microservice
    driver_result = invoke_http("http://localhost:5001/driver/" + str(delivery_result['data']['driver_ID']), method='GET')
    
    # 6. Check the driver result; if a failure, send it to the error microservice.
    code = driver_result["code"]
    if code not in range(200, 300):
        print('\n\n-----Publishing the (driver error) message with routing_key=DriverCompleteDelivery.driver.error-----')
        message=json.dumps(delivery_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="DriverCompleteDelivery.driver.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nDelivery MS call status ({:d}) published to the RabbitMQ Exchange:".format(code), driver_result)

        return {
            "code": 502,
            "data": {"driver_result": driver_result},
            "message": "Failed to retrieve driver data, sent for error handling."
        }

    delivery_driver = driver_result['data']['driver_name']   
    # print(delivery_driver)


    #6. Invoke Customer Notification AMQP
    customer_and_driver_msg = "Delivery Completed! \n\n" + "Delivery Order ID: " + str(delivery_result['data']['delivery_ID']) + " was delivered by " + str(delivery_driver) + " to " + str(delivery_result['data']['receiver_name']) + " on " + str(delivery_result['data']['last_updated'])

    messages = json.dumps({
            "customer_message": customer_and_driver_msg,
            "driver_message": customer_and_driver_msg         
    })

    print('\n\n-----Publishing the (customer) message with routing_key=customer.order-----')
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="customer.CompleteDelivery", body=messages)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="driver.CompleteDelivery", body=messages)
    
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
    app.run(host="0.0.0.0", port=5103, debug=True)
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
