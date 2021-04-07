# 1. determine which driver is free for that date, that time slot (list of drivers)
# 2. get their schedules for those drivers who are free for that day
# 3. create a priority queue in accordance to how free they are (the number of false in their schedule for that day)
# 4. select the driver who is free

from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import datetime

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

HOST = '0.0.0.0'
PORT = 5104

driver_URL = "http://localhost:5001/driver/"
schedule_URL = "http://localhost:5004/schedule/"
delivery_URL = "http://localhost:5000/delivery"

@app.route("/schedule_driver/<string:delivery_date>/<string:timeslot>", methods=['GET'])
def schedule_driver(delivery_date, timeslot):
    # data format: date is YYYY-MM-DD, time is eg. 8_to_10
    # should check for format error here
    
    try:
        datetime.datetime.strptime(delivery_date, '%Y-%m-%d')
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Incorrect data format, should be YYYY-MM-DD"
        })

    
    allowed_timeslots=['8_to_10', '10_to_12', '12_to_2', '2_to_4', '4_to_6']

    if timeslot not in allowed_timeslots:
        return jsonify ({
            "code": 501,
            "message": "Incorrect timeslot format, please select from " + str(allowed_timeslots)
        })

    query_result = get_available_drivers(delivery_date, timeslot)
    
    if query_result['code'] not in range (200,300):
        return query_result

    #print("next")
    #print(query_result)
    selected_driver= choose_best(query_result)

    #print(selected_driver)
    return {
        "code": 200,
        "data": selected_driver        
    }



def get_available_drivers(delivery_date, timeslot):
    # 1. invoke schedule MS to determine which driver is free for selected day + timeslot
    # Invoke the schedule microservice
    print('\n-----Invoking schedule microservice-----')

    schedule_result = invoke_http(schedule_URL + '/date/' + delivery_date + '/' + timeslot, method='GET')
    print('schedule result: ' + str(schedule_result))

    # 3. Check the delivery result; if a failure, send it to the error microservice.
    code = schedule_result["code"]
    if code not in range(200, 300):
        # print('\n\n-----Invoking error microservice as delivery fails-----')
        # invoke_http("http://localhost:5007/error", method="POST", json=schedule_result)

        print('\n\n-----Publishing the (schedule error) message with routing_key=scheduler.schedule.error-----')
        # message=json.dumps(schedule_result)
        error_message = {
            "code": 502,
            "data": {"schedule_result": schedule_result},
            "message": "Failure to retrieve available drivers, sent for error handling."
        }
        message = json.dumps(error_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="scheduler.schedule.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Delivery status ({:d}) published to the RabbitMQ Exchange:".format(code), error_message)

        return error_message

    return {
        "code": 201,
        "data": {
            "schedule_result": schedule_result,
        }
    }


def choose_best(query_result):
    list_of_schedules= query_result['data']['schedule_result']['data']['schedules']
    #print("reached!")
    #print(list_of_schedules)

    mydict={}
    for i in range(len(list_of_schedules)):
        current_schedule=list_of_schedules[i]
        #print(current_schedule)

        counter=0
        timeslots_to_check=['t_8_to_10', 't_10_to_12', 't_12_to_2', 't_2_to_4', 't_4_to_6']
        for timeslot in timeslots_to_check:
            if current_schedule[timeslot]==False:
                counter+=1
        
        mydict[i]=counter
    
    #print(mydict)

    max_value=max(mydict.values())

    for key in mydict:
        if mydict[key]==max_value:
            return list_of_schedules[key]




# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for scheduling a driver")
    app.run(host=HOST, port=PORT, debug=True)
    print(f'App running on {HOST}:{PORT}')
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
