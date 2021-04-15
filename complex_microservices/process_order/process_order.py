from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests

from os import environ
from invokes import invoke_http

import amqp_setup
import pika
import json

HOST = "0.0.0.0"
PORT = 5100

app = Flask(__name__)
CORS(app)

############################################################################################################
# Process Order Sequence
# 1. UI: get order details through localStorage
# 2. invoke process order through POST & pass in the data retrieved
# 3. process order checks for validity of json format passed it
# 4. process order invokes Payment MS to validate payment_status & get payment details
# 5. process order invokes Scheduler Function to schedule assign appropriate driver
# 6. process order invokes schedule to update the assigned driver's schedule
# 7. process order invokes Driver MS to get assigned driver information
# 8. process order invokes Customer MS for customer information
# 9. process order constructs relevant json data and invokes Delivery MS to create delivery order through POST
# 10. process order calls AMQP Publisher to notify Customer subscriber MS (inform of new delivery) 
# and Driver subscriber MS (to inform of new Job)
##############################################################################################################

payment_URL = environ.get('paymentURL') or "http://127.0.0.1:4242/checkout_session"
delivery_URL = environ.get('deliveryURL') or "http://127.0.0.1:5000/delivery"
driver_URL = environ.get('driverURL') or "http://127.0.0.1:5001/driver"
customer_URL = environ.get('customerURL') or "http://127.0.0.1:5002/customer"
schedule_URL = environ.get('scheduleURL') or "http://127.0.0.1:5004/schedule"
schedule_driver_URL = environ.get('ScheduleDriverURL') or "http://127.0.0.1:5104/schedule_driver"


@app.route("/process_order/<string:customer_ID>", methods=['POST'])
def process_order(customer_ID):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            data = request.get_json()

            session_id, delivery_data = data['session_id'], data['delivery_data']

            # do the actual work
            # 1. Send order info {delivery order}
            order = processOrderCreation(session_id, delivery_data, customer_ID)
            if order:
                send_notification(order)
                return data

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)

            return jsonify({
                "code": 500,
                "message": "process_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processOrderCreation(session_id, delivery_data, customer_ID):
    # 1. invoke payment MS using session id to get payment details
    # Invoke the payment microservice
    print('\n-----Invoking payment microservice-----')
    payment_data = invoke_http(payment_URL + "/" + session_id, method='GET')
    print('payment_results:', str(payment_data))

    code = payment_data['code']
    if code not in range(200, 300):
        error_message = {
            "code": 501,
            "data": {"payment_data": payment_data},
            "message": "Failed to get payment session details using Payment Microservice(GET), sent for error handling."
        }
        print('\n\n-----Publishing the (payment error) message with routing_key=login.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="login.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

    #4. Retrieve the payment_status for verification
    payment_status = payment_data['payment_status']

    #check if payment status is paid, if not raise error
    if payment_status == "unpaid":
        return jsonify({
            "code": "400",
            "message": "The payment status of the delivery order is unpaid."
        }), 400
    
    #5. Invoke schedule_driver to allocate the driver for the delivery

    date = delivery_data['date']
    time = delivery_data['time']
    url = schedule_driver_URL + "/" + date + "/" + time

    print('\n-----Invoking schedule_driver microservice-----')
    selected_driver = invoke_http(schedule_driver_URL + "/" + str(date) + "/" + str(time), method='GET')
    # print('Selected_driver: ' + str(selected_driver) + "\n")

    # check the schedule_driver results: if failure send to error microservice for logging
    code = selected_driver['code']
    if code not in range(200, 300):
        error_message = {
            "code": 501,
            "data": {"selected_driver": selected_driver},
            "message": "Failed to get allocated driver using Schedule Driver Microservice (GET), sent for error handling."
        }
        print('\n\n-----Publishing the (schedule driver error) message with routing_key=login.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="login.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

    #Initialise the driver ID and data for updating of their schedule
    selected_schedule_ID = selected_driver['data']['SID']
    updated_schedule = selected_driver['data']

    # remove SID from POST body data
    updated_schedule.pop('SID')
    updated_schedule['delivery_date'] = date
    #remove SID as it will be passed through the URL rather than the body
    updated_schedule["t_"+time] = True

    #6. Invoke schedule to update allocated driver's schedule
    print('\n-----Invoking Schedule Microservice-----')
    driver_schedule_updated = invoke_http(schedule_URL + "/" + str(selected_schedule_ID), method='PUT', json=updated_schedule)

    #check the driver updated results: if failure send to error microservice for logging
    code = driver_schedule_updated['code']
    if code not in range(200, 300):
        error_message = {
            "code": 501,
            "data": {"driver_schedule_updated": driver_schedule_updated},
            "message": "Failed to update allocated driver using Schedule Microservice (PUT), sent for error handling."
        }
        print('\n\n-----Publishing the (update schedule error) message with routing_key=schedule.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="schedule.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

    #9. Invoke Delivery Microservice to create new Delivery order using POST

    delivery_entry = {
        "driver_ID": selected_driver['data']['driver_ID'],
        "customer_ID": customer_ID,
        "delivery_date": delivery_data['date'],
        "timeslot": delivery_data['time'],
        "pickup_location": delivery_data['pickup'] + ", Singapore " + delivery_data['pickupPostalCode'],
        "destination": delivery_data['destination'] + ", Singapore " + delivery_data['destinationPostalCode'],
        "delivery_item": delivery_data['delivery_item'],
        "description": delivery_data['description'],
        "payment_amount": payment_data['amount_total'],
        "payment_status": payment_status,
        "receiver_name": delivery_data['receiver_name']
    }

    print('\n-----Invoking Delivery Microservice-----')
    delivery_created = invoke_http(delivery_URL, method='POST', json=delivery_entry)

    #check the newly created delivery order: if failure send to error microservice for logging
    code = delivery_created['code']
    if code not in range(200, 300):
        error_message = {
            "code": 501,
            "data": {"delivery_created": delivery_created},
            "message": "Failed to create Delivery Order using Delivery Microservice (POST), sent for error handling."
        }
        print('\n\n-----Publishing the (delivery error) message with routing_key=delivery.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="delivery.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
        
    return delivery_created


def send_notification(order):
    print(order)
    driver_ID = order['data']['driver_ID']
    customer_ID = order['data']['customer_ID']
    delivery_ID = order['data']['delivery_ID']

    #1. Invoke the Driver Microservice to get the chat ID of the allocated driver
    print('\n-----Invoking Driver Microservice-----')
    driver_data = invoke_http(driver_URL + "/" + str(driver_ID), method='GET')

    # #check the driver's data: if failure send to error microservice for logging
    code = driver_data['code']
    if code not in range(200, 300):
        error_message = {
            "code": 501,
            "data": {"driver_data": driver_data},
            "message": "Failed to retrieve Driver from Driver Microservice (GET), sent for error handling."
        }
        print('\n\n-----Publishing the (driver error) message with routing_key=driver.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="driver.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
        return error_message
    
    #2. Invoke the Customer Microservice to get the chat ID of the customer
    print('\n-----Invoking Customer Microservice-----')
    customer_data = invoke_http(customer_URL + "/" + str(customer_ID), method='GET')

    # #check the customer's data: if failure send to error microservice for logging
    code = customer_data['code']
    if code not in range(200, 300):
        error_message = {
            "code": 501,
            "data": {"customer_data": customer_data},
            "message": "Failed to retrieve Customer from Customer Microservice (GET), sent for error handling."
        }
        print('\n\n-----Publishing the (driver error) message with routing_key=customer.error-----')
        message=json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="customer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
        return error_message

    #invoke the notification AMQP to inform customer of new delivery order

    driver_tele_chat_ID = driver_data['data']['tele_chat_ID']
    customer_tele_chat_ID = customer_data['data']['tele_chat_ID']

    receiver_name = order['data']['receiver_name']
    created = order['data']['created']

    customer_message = "Delivery Created! +\n\nDelivery Order ID: " + str(delivery_ID) + " to " + str(receiver_name) +" has been successfully created on " + str(created) + "\nPlease proceed to 'View My Deliveries' to catch a glimpse!"
    driver_message = "You have a new delivery order! \n\nDelivery Order ID: " + str(delivery_ID) + " has been successfully created on " + str(created) + "\nPlease proceed to 'View my Schedule' to catch a glimpse!"

    messages = json.dumps({
            "customer_message": customer_message,
            "customer_tele_chat_ID": customer_tele_chat_ID,
            "driver_message": driver_message,
            "driver_tele_chat_ID": driver_tele_chat_ID
    })

    print('\n\n-----Publishing the (customer & driver) message with routing_key=customer.DeliveryCreated and routing_key=driver.DeliveryCreated-----')
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="customer.DeliveryCreated", body=messages)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="driver.DeliveryCreated", body=messages)

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host=HOST, port=PORT, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
