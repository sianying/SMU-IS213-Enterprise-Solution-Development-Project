# Process workflow

# 1. customer logs into his account, a customer id is provided
# 4. invoke delivery microservice to return all deliveries that match the customer's id
# 5. for each job, return all delivery details
# 6. for each delivery returned, use the driver id and invoke driver microservice to retrieve details of each driver
# 7. driver microservice returns driver details (name, teleid, mobile, email)
# 8. after collating the info, display everything on UI

from flask import Flask, request, jsonify
from flask_cors import CORS

import os 
import requests

from os import environ
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

deliveryURL=environ.get('deliveryURL')
driverURL=environ.get('driverURL')

# Main function that calls other functions
@app.route("/customer_view_details/<int:customer_ID>", methods=['GET'])
def customer_view_details(customer_ID):
    try:
        result2= retrieve_all_deliveries(customer_ID)

        # 3. for each job, add the customer name and customer contact. Next, add driver name and contact no.
        # Once everything is ready, return the final_result. 
        list_of_deliveries=result2['data']['delivery_result']  

        # print("List of deliveries:")
        # print(list_of_deliveries)

        driver_result = invoke_http(driverURL, method='GET')
        # print('1st part done!')
        #print(driver_result)

        list_of_drivers=driver_result['data']['drivers']

        # print("list of drivers:")
        # print(list_of_drivers)

        for delivery in list_of_deliveries:
            driver_id=delivery['driver_ID']
            print(driver_id)
            for driver in list_of_drivers:
                if driver_id==driver['driver_ID']:
                    delivery['driver_name']=driver['driver_name']
                    delivery['driver_mobile']=driver['driver_mobile']
                    delivery['driver_email']= driver['driver_email']
                    delivery['driver_teleID']=driver['driver_teleID']
                    break
        # print("")
        # print(final_result)
        # print("")
        # print(list_of_deliveries)



        return {
            "code": 202,
            "data": {
                "customer_view_details": list_of_deliveries
            }
        }

    except Exception as e:
        # Unexpected error in code

        return jsonify({
            "code": 500,
            "message": "customer_view_details.py internal error"
        }), 500


def retrieve_all_deliveries(customer_ID):
    # 2. Invoke the delivery microservice
    #print('\n-----Invoking delivery microservice-----')
    delivery_result = invoke_http(deliveryURL+ "/customer/" + str(customer_ID), method='GET')
    print('delivery_result:', delivery_result)

    # 3. Check the delivery result; if a failure, send it to the error microservice.
    code = delivery_result["code"]
    if code not in range(200, 300):
        print('\n\n-----Publishing the (delivery error) message with routing_key=CustomerViewDetails.delivery.error-----')
        message=json.dumps(delivery_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="CustomerViewDetails.delivery.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nDelivery MS Call status ({:d}) published to the RabbitMQ Exchange:".format(code), delivery_result)

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

# def add_driver_details(delivery):

#      # 2. Invoke the driver microservice
#     #print('\n-----Invoking driver microservice-----')
#     driver_result = invoke_http("http://localhost:5001/driver/" + str(driver_ID), method='GET')
#     print('driver_result:', driver_result)

#     # 3. Check the delivery result; if a failure, send it to the error microservice.
#     code = driver_result["code"]
#     if code not in range(200, 300):
#     #     print('\n\n-----Publishing the (driver error) message with routing_key=CustomerViewDetails.driver.error-----')
#     #     message=json.dumps(driver_result)
#     #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="CustomerViewDetails.driver.error", 
#     #         body=message, properties=pika.BasicProperties(delivery_mode = 2))

#         #print("\nDriver MS Call status ({:d}) published to the RabbitMQ Exchange:".format(code), driver_result)

#         print('\n\n-----Invoking error microservice as delivery fails-----')
#         invoke_http("http://localhost:5007/error", method="POST", json=driver_result)
#         # - reply from the invocation is not used; 
#         # continue even if this invocation fails
#         print("Driver MS call status ({:d}) sent to the error microservice:".format(
#             code), driver_result)

#         return {
#             "code": 502,
#             "data": {"driver_result": driver_result},
#             "message": "Failed to retrieve driver's details, sent for error handling."
#         }

#     #adding driver details to be added in the end
#     delivery['driver_name']=driver_result['data']['driver_name']
#     delivery['driver_mobile']=driver_result['data']['driver_mobile']
#     delivery['driver_email']= driver_result['data']['driver_email']

#     return delivery


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
        # print(list_of_deliveries)

      