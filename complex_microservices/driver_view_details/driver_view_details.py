#driver views job details, call google distance matrix api

# 1. driver wants to view job details, clicks on a particular job on the UI
# 2. HTTP GET request to delivery microservice and retrieve existing delivery details from db
# 3. delivery microservice returns job details
# 4. Based on the pickup location and destination, call Google Distance Matrix API and return distance
# 5. Google Distance API returns distance and estimated journey duration to complex microservice
# 6. Complex microservice collates all the information, javascript will process the json returned and display it on the UI

from flask import Flask, request, jsonify
from flask_cors import CORS


import os
import requests
import google

from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

# Main function that calls other functions
@app.route("/driver_view_details/<int:delivery_ID>", methods=['GET'])
def driver_job_details(delivery_ID):
    try:
        # do the actual work
        # 1. get info already stored in database
        intermediate_result = get_existing_info(delivery_ID)

        #print(intermediate_result)

        # 2. get additional info by calling the google distance api
        final_result=get_more_info(intermediate_result)

        return jsonify(final_result), final_result["code"]

    except Exception as e:
        # Unexpected error in code

        return jsonify({
            "code": 500,
            "message": "driver_view_details.py internal error"
        }), 500



def get_existing_info(delivery_ID):
    # 2. Invoke the delivery microservice
    print('\n-----Invoking delivery microservice-----')
    delivery_result = invoke_http("http://localhost:5000/delivery/" + str(delivery_ID), method='GET')
    print('delivery_result:', delivery_result)

    # 3. Check the delivery result; if a failure, send it to the error microservice.
    code = delivery_result["code"]
    if code not in range(200, 300):
        print('\n\n-----Publishing the (delivery error) message with routing_key=DriverViewDetails.delivery.error-----')
        # message=json.dumps(delivery_result)
        error_message = {
            "code": 501,
            "data": {"delivery_result": delivery_result},
            "message": "Delivery update failure, sent for error handling."
        }
        message = json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="DriverViewDetails.delivery.error", body=message, properties=pika.BasicProperties(delivery_mode = 2))

        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Delivery MS Call status ({:d}) published to the RabbitMQ Exchange:".format(code), error_message)




        # print('\n\n-----Invoking error microservice as delivery fails-----')
        # invoke_http("http://localhost:5007/error", method="POST", json=delivery_result)
        # # - reply from the invocation is not used; 
        # # continue even if this invocation fails
        # print("Delivery status ({:d}) sent to the error microservice:".format(
        #     code), delivery_result)

        return error_message

    return {
        "code": 201,
        "data": {
            "delivery_result": delivery_result,
        }
    }

# call google distance api to get estimated time taken
# might have to call api twice, but for now just do once

def get_more_info(delivery):
    api_key = 'AIzaSyCOb2n2zlVPQd7Jd6eGY0HoMO9Md4VLtqU'   
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"

    #get from json returned in the 1st function
    origins=delivery['data']['delivery_result']['data']['pickup_location']
    #print(origins)
    destination=delivery['data']['delivery_result']['data']['destination']
    #print(destination)

    response = requests.get(url + "origins=" + origins + "&destinations=" + destination + "&key=" + api_key)
    response_json=response.json()

    #print("until here ok!")

    print(response_json)

    if response_json['status']!='OK':
        print('\n\n-----Publishing the (API call error) message with routing_key=DriverViewDetails.API.error-----')
        # message=json.dumps(response_json)
        error_message = {
            "code": 400,
            "data": {"api_call_result": response_json},
            "message": "API Call failure, sent for error handling."
        }
        message = json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="DriverViewDetails.API.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nAPI Call status ({:d}) published to the RabbitMQ Exchange:".format(
            response_json['status']), error_message)

        # print('\n\n-----Invoking error microservice as api call fails-----')
        # invoke_http("http://localhost:5007/error", method="POST", json=response)
        # # - reply from the invocation is not used; 
        # # continue even if this invocation fails
        # print("Details of API Call ({:d}) sent to the error microservice:".format(response_json['status']), response_json)

        return error_message

    distance_in_km= round(response_json['rows'][0]['elements'][0]['distance']['value']/1000, 1)
    duration_in_min= response_json['rows'][0]['elements'][0]['duration']['text']

    delivery['distance_in_km']=distance_in_km
    delivery['duration_in_min']=duration_in_min

    return {
        "code": 201,
        "data": {
            "api_call_result": delivery,
        }
    }

# SAMPLE JSON CODE
#{'destination_addresses': ['21 Lower Kent Ridge Rd, University Hall, Singapore 119077'], 'origin_addresses': ['81 Victoria St, Singapore 188065'], 'rows': [{'elements': [{'distance': {'text': '6.3 mi', 'value': 10187}, 'duration': {'text': '15 mins', 'value': 913}, 'status': 'OK'}]}], 'status': 'OK'}


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for driver viewing delivery details...")
    app.run(host="0.0.0.0", port=5101, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
