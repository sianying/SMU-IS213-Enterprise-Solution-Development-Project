from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
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

#book_URL = "http://localhost:5000/book"
# order_URL = "http://localhost:5001/order"
# shipping_record_URL = "http://localhost:5002/shipping_record"
#activity_log_URL = "http://localhost:5003/activity_log"
#error_URL = "http://localhost:5004/error"

payment_URL = "http://localhost:4242/checkout_session"
delivery_URL = "http://localhost:5000/delivery"
driver_URL = "http://localhost:5001/driver"
customer_URL = "http://localhost:5002/customer"
schedule_URL = "http://localhost:5004/schedule"
schedule_driver_URL = "http://localhost:5104/schedule_driver"

@app.route("/process_order/<string:customer_ID>", methods=['POST'])
def process_order(customer_ID):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            #session id + delivery data
            data = request.get_json()
            print("\nReceived an data in JSON:", data)
            session_id, delivery_data = data['session_id'], data['delivery_data']

            # do the actual work
            # 1. Send order info {delivery order}
            order = processOrderCreation(session_id, delivery_data, customer_ID)
            if order:
                order_ID = order['delivery_ID']
                send_notification(order_ID)

                print(data)
                return data
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

    #4. Retrieve the payment_status for verification
    payment_status = payment_data['payment_status']

    #check if payment status is paid, if not raise error
    if payment_status == "unpaid":
        return jsonify({
            "code": "400",
            "message": "The payment status of the delivery order is unpaid."
        }), 400
    
    #5. Invoke schedule_driver to allocate the driver for the delivery
    #have not implement calendar + selection of delivery date
    print('\n-----Invoking schedule_driver microservice-----')
    #hardcode date and time first: "2020-06-1", "8_to_10"
    # date = "2020-06-01"
    # time = "8_to_10"
    date = delivery_data['date']
    time = delivery_data['time']
    url = schedule_driver_URL + "/" + date + "/" + time
    print(url)
    selected_driver = invoke_http(schedule_driver_URL + "/" + str(date) + "/" + str(time), method='GET')
    print('Selected_driver: ' + str(selected_driver) + "\n")

    # check the schedule_driver results: if failure send to error microservice for logging
    code = selected_driver['code']
    if code not in range(200,300):
        # print('\n\n-----Invoking error microservice as schedule driver fails-----')
        #send to error microservice via rabbitMQ
        return 

    #Initialise the driver ID and data for updating of their schedule
    selected_schedule_ID = selected_driver['data']['SID']
    updated_schedule = selected_driver['data']
    print(updated_schedule)
    # remove SID from POST body data
    updated_schedule.pop('SID')
    updated_schedule['delivery_date'] = date
    #remove SID as it will be passed through the URL rather than the body
    updated_schedule["t_"+time] = True
    # timeslots = ['8_to_10', '10_to_12', '12_to_2', '2_to_4', '4_to_6']
    # for timeslot in timeslots:
    #     timeslot = "t_" + timeslot
    #     if time == updated_schedule[timeslot]:
    #         updated_schedule[timeslot] = time
    #6. Invoke schedule to update allocated driver's schedule
    print('\n-----Invoking Schedule Microservice-----')
    driver_schedule_updated = invoke_http(schedule_URL + "/" + str(selected_schedule_ID), method='PUT', json=updated_schedule)
    print("Updated Driver's schedule: " + str(driver_schedule_updated) + "\n")

    #check the driver updated results: if failure send to error microservice for logging
    code = driver_schedule_updated['code']
    if code not in range(200, 300):
        #send over to error microservice for logging
        return
    
    #7. Invoke the Driver Microservice to get the details of the allocated driver
    # print('\n-----Invoking Driver Microservice-----')
    # driver_data = invoke_http(driver_URL + "/" + str(selected_driver_ID))
    # print("Updated Driver's schedule"+ str(driver_data) + "\n")

    # #check the driver's data: if failure send to error microservice for logging
    # code = driver_schedule_updated['code']
    # if code not in range(200, 300):
    #     #send over to error microservice for logging
    #     return
    
    #8. Invoke the Customer Microservice to get the details of the customer
    # print('\n-----Invoking Customer Microservice-----')
    # customer_data = invoke_http(customer_URL + "/" + customer_ID)
    # print("Customer's information: "+ str(customer_data) + "\n")

    # #check the customer's data: if failure send to error microservice for logging
    # code = customer_data['code']
    # if code not in range(200, 300):
    #     #send over to error microservice for logging
    #     return

    #9. Invoke Delivery Microservice to create new Delivery order using POST
    #create the POST data

    delivery_entry = {
        "driver_ID": selected_driver['data']['driver_ID'],
        "customer_ID": customer_ID,
        "delivery_date": delivery_data['date'],
        "timeslot": delivery_data['time'],
        "pickup_location": delivery_data['pickup'] + delivery_data['pickupPostalCode'],
        "destination": delivery_data['destination'] + delivery_data['destinationPostalCode'],
        "delivery_item": delivery_data['delivery_item'],
        "description": delivery_data['description'],
        "payment_amount": payment_data['amount_total'],
        "payment_status": payment_status,
        "receiver_name": delivery_data['receiver_name']
    }

    print('\n-----Invoking Delivery Microservice-----')
    print(delivery_URL )
    delivery_created = invoke_http(delivery_URL, method='POST', json=delivery_entry)
    print("New Delivery created: " + str(delivery_created) + "\n")

    #check the newly created delivery order: if failure send to error microservice for logging
    code = delivery_created['code']
    if code not in range(200, 300):
        #send over to error microservice for logging
        return
    
    return delivery_created


    # # Check the order result; if a failure, send it to the error microservice.
    # code = order_result["code"]
    # message = json.dumps(order_result)

    # if code not in range(200, 300):
    #     # Inform the error microservice
    #     #print('\n\n-----Invoking error microservice as order fails-----')
    #     print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

    #     # invoke_http(error_URL, method="POST", json=order_result)
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
    #         body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
    #     # make message persistent within the matching queues until it is received by some receiver 
    #     # (the matching queues have to exist and be durable and bound to the exchange)

    #     # - reply from the invocation is not used;
    #     # continue even if this invocation fails        
    #     print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
    #         code), order_result)

    #     # 7. Return error
    #     return {
    #         "code": 500,
    #         "data": {"order_result": order_result},
    #         "message": "Order creation failure sent for error handling."
    #     }

    # # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # # In http version, we first invoked "Activity Log" and then checked for error.
    # # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # # and a message sent to “Error” queue can be received by “Activity Log” too.

    # else:
    #     # 4. Record new order
    #     # record the activity log anyway
    #     #print('\n\n-----Invoking activity_log microservice-----')
    #     print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')        

    #     # invoke_http(activity_log_URL, method="POST", json=order_result)            
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
    #         body=message)
    
    # print("\nOrder published to RabbitMQ Exchange.\n")
    # # - reply from the invocation is not used;
    # # continue even if this invocation fails
    
    # # 5. Send new order to shipping
    # # Invoke the shipping record microservice
    # print('\n\n-----Invoking shipping_record microservice-----')    
    
    # shipping_result = invoke_http(
    #     shipping_record_URL, method="POST", json=order_result['data'])
    # print("shipping_result:", shipping_result, '\n')

    # # Check the shipping result;
    # # if a failure, send it to the error microservice.
    # code = shipping_result["code"]
    # if code not in range(200, 300):
    #     # Inform the error microservice
    #     #print('\n\n-----Invoking error microservice as shipping fails-----')
    #     print('\n\n-----Publishing the (shipping error) message with routing_key=shipping.error-----')

    #     # invoke_http(error_URL, method="POST", json=shipping_result)
    #     message = json.dumps(shipping_result)
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error", 
    #         body=message, properties=pika.BasicProperties(delivery_mode = 2))

    #     print("\nShipping status ({:d}) published to the RabbitMQ Exchange:".format(
    #         code), shipping_result)

    #     # 7. Return error
    #     return {
    #         "code": 400,
    #         "data": {
    #             "order_result": order_result,
    #             "shipping_result": shipping_result
    #         },
    #         "message": "Simulated shipping record error sent for error handling."
    #     }

    # # 7. Return created order, shipping record
    # return {
    #     "code": 201,
    #     "data": {
    #         "order_result": order_result,
    #         "shipping_result": shipping_result
    #     }
    # }

def send_notification(order_ID):
    #invoke the notification AMQP to inform customer of new delivery order
    # print('\n\n-----Invoking customer_notification microservice-----')
    customer_message = "Your delivery order #" + str(order_ID) + " has been successfully created! \n" + "Please proceed to 'View My Deliveries' to have a glimpse."
    driver_message = "You have a new delivery order #" + str(order_ID) + "!\n" + "Please proceed to 'View My Deliveries' or 'View my Schedule' to have a glimpse."

    messages = json.dumps({
            "customer_message": customer_message,
            "driver_message": driver_message          
    })

    print('\n\n-----Publishing the (customer) message with routing_key=customer.order-----')
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
