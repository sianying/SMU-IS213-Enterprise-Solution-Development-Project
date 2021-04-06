# Process workflow

# 1. customer logs into his account, a customer id is provided
# 2. invoke customer microservice to retrieve customer details
# 3. customer microservice returns customer name and contact number ONLY
# 4. invoke delivery microservice to return all jobs that match the customer's id
# 5. for each job, return relevant job details only: timeslot, driver_id, pickup location, destination
# 6. using the driver_id returned earlier, invoke driver microservice retrieving details of driver
# 7. driver microservice returns driver name and contact number
# 8. for each job, display timeslot, customer_name, customer contact, driver name, driver contact, pickup location and destination, status on UI

from flask import Flask, request, jsonify
from flask_cors import CORS

import os 
import requests

from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

# Main function that calls other functions
@app.route("/customer_view_details/<int:customer_ID>", methods=['GET'])
def customer_view_details(customer_ID):
    try:
        # Do the actual work (3 steps)
        
        # 1. get info stored in customer MS
        #result 1 is a list in the form [name, phone no, email, tele id]
        # result1 = get_customer_info(customer_ID)

        # 2. retrieve all jobs from delivery MS matching the customer ID
        result2= retrieve_all_deliveries(customer_ID)

        # 3. for each job, add the customer name and customer contact. Next, add driver name and contact no.
        # Once everything is ready, return the final_result. 
        list_of_deliveries=result2['data']['delivery_result']  

        # print("List of deliveries:")
        # print(list_of_deliveries)

        final_result=[]
        print("start")
        for delivery in list_of_deliveries:
            # print("")
            # print ("initial delivery")
            # print(delivery)
            # delivery['customer_name']= result1[0]
            # delivery['customer_mobile']= result1[1]
            # delivery['customer_email']= result1[2]
            # delivery['customer_teleid']= result1[3]

            # print("")
            # print("final delivery")
            # print(delivery)
            add_driver_details(delivery)

            final_result.append(delivery)
        print("end")
        # print("")
        # print(final_result)

        return {
            "code": 202,
            "data": {
                "customer_view_details": final_result,
            }
        }

    except Exception as e:
        # Unexpected error in code

        return jsonify({
            "code": 500,
            "message": "customer_view_details.py internal error"
        }), 500


# def get_customer_info(customer_ID):
#     # 2. Invoke the customer microservice
#     print('\n-----Invoking customer microservice-----')
#     customer_result = invoke_http("http://localhost:5002/customer/" + str(customer_ID), method='GET')
#     print('customer_result:', customer_result)

#     # 3. Check the delivery result; if a failure, send it to the error microservice.
#     code = customer_result["code"]
#     if code not in range(200, 300):
#         print('\n\n-----Publishing the (customer error) message with routing_key=CustomerViewDetails.customer.error-----')
#         message=json.dumps(customer_result)
#         amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="CustomerViewDetails.customer.error", 
#             body=message, properties=pika.BasicProperties(delivery_mode = 2))

#         print("\nCustomer MS call status ({:d}) published to the RabbitMQ Exchange:".format(
#             code), customer_result)

#         # print('\n\n-----Invoking error microservice as delivery fails-----')
#         # invoke_http("http://localhost:5007/error", method="POST", json=customer_result)
#         # # - reply from the invocation is not used; 
#         # # continue even if this invocation fails
#         # print("Delivery status ({:d}) sent to the error microservice:".format(
#         #     code), customer_result)

#         return {
#             "code": 501,
#             "data": {"customer_result": customer_result},
#             "message": "Failed to retrieve customer data, sent for error handling."
#         }

#     data=customer_result['data']
#     returned_list=[data['CName'], data['CMobile'], data['CEmail'], data['CTeleID']]
#     print(returned_list)

#     return returned_list
    # return {
    #     "code": 201,
    #     "data": {
    #         "customer_result": customer_result,
    #     }
    # }

def retrieve_all_deliveries(customer_ID):
    # 2. Invoke the delivery microservice
    print('\n-----Invoking delivery microservice-----')
    delivery_result = invoke_http("http://localhost:5000/delivery/customer/" + str(customer_ID), method='GET')
    #print('delivery_result:', delivery_result)

    # 3. Check the delivery result; if a failure, send it to the error microservice.
    code = delivery_result["code"]
    if code not in range(200, 300):
        #print('\n\n-----Publishing the (delivery error) message with routing_key=CustomerViewDetails.delivery.error-----')
        message=json.dumps(delivery_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="CustomerViewDetails.delivery.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        #print("\nDelivery MS Call status ({:d}) published to the RabbitMQ Exchange:".format(code), delivery_result)

        # print('\n\n-----Invoking error microservice as delivery fails-----')
        # invoke_http("http://localhost:5007/error", method="POST", json=delivery_result)
        # # - reply from the invocation is not used; 
        # # continue even if this invocation fails
        # print("Delivery status ({:d}) sent to the error microservice:".format(
        #     code), delivery_result)

        return {
            "code": 502,
            "data": {"delivery_result": delivery_result},
            "message": "Failed to retrieve the customer's list of deliveries, sent for error handling."
        }

    return {
        "code": 201,
        "data": {
            "delivery_result": delivery_result['data']['deliveries'],
        }
    }

def add_driver_details(delivery):
    driver_ID=delivery['driver_ID']

    # 2. Invoke the driver microservice
    print('\n-----Invoking driver microservice-----')
    driver_result = invoke_http("http://localhost:5001/driver/" + str(driver_ID), method='GET')
    print('driver_result:', driver_result)

    # 3. Check the delivery result; if a failure, send it to the error microservice.
    code = driver_result["code"]
    if code not in range(200, 300):
        print('\n\n-----Publishing the (driver error) message with routing_key=CustomerViewDetails.driver.error-----')
        message=json.dumps(driver_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="CustomerViewDetails.driver.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        #print("\nDriver MS Call status ({:d}) published to the RabbitMQ Exchange:".format(code), driver_result)

        # print('\n\n-----Invoking error microservice as delivery fails-----')
        # invoke_http("http://localhost:5007/error", method="POST", json=driver_result)
        # # - reply from the invocation is not used; 
        # # continue even if this invocation fails
        # print("Driver MS call status ({:d}) sent to the error microservice:".format(
        #     code), driver_result)

        return {
            "code": 502,
            "data": {"driver_result": driver_result},
            "message": "Failed to retrieve driver's details, sent for error handling."
        }

    #adding driver details to be added in the end
    delivery['driver_name']=driver_result['data']['driver_name']
    delivery['driver_mobile']=driver_result['data']['driver_mobile']
    delivery['driver_email']= driver_result['data']['driver_email']

    return delivery


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
            " for customer viewing delivery details...")
    app.run(host="0.0.0.0", port=5102, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
