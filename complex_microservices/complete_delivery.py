#driver complete a job
#ber zonghan

# Done under "driver views job details" complex microservice
# 1. Driver filters deliveries by customer id. 
# 2. Delivery microservice returns a set of deliveries.
# 3. On the UI, he selects a delivery.
# 4. The delivery microservice returns the selected delivery.

# Need to do
# 5. He presses a button to verify completion of delivery. Delivery microservice updates delivery_status by id
# 6. Delivery returns the necessary info (id, driver name, date, timeslot, updated status).
# 7. Notify driver and customer (who made the order) of successful completion. 

from flask import Flask, request, jsonify
from flask_cors import CORS

import os

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# Main function that calls other functions
@app.route("/complete_delivery/<int:delivery_ID>", methods=['GET'])
def complete_delivery(delivery_ID):
    if request.is_json:
        try:
            delivery = request.get_json()
            print("\nThe following delivery is complete:", delivery)

            # do the actual work
            # 1. Send order info {cart items}
            result = update_delivery_status(delivery)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code

            return jsonify({
                "code": 500,
                "message": "delivery_complete.py internal error"
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


# call delivery microservice to update and return new delivery status
def update_delivery_status(delivery):
    # 2. Invoke the delivery microservice
    print('\n-----Invoking delivery microservice-----')
    delivery_result = invoke_http("http:localhost:5000/delivery/" + str(delivery.delivery_ID), method='PUT', json=delivery)
    print('delivery_result:', delivery_result)

    # 3. Check the delivery result; if a failure, send it to the error microservice.
    code = delivery_result["code"]
    if code not in range(200, 300):
        print('\n\n-----Invoking error microservice as delivery fails-----')
        invoke_http("http:localhost:5007/error", method="POST", json=delivery_result)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Delivery status ({:d}) sent to the error microservice:".format(
            code), delivery_result)

        return {
            "code": 500,
            "data": {"delivery_result": delivery_result},
            "message": "Delivery update failure, sent for error handling."
        }
        
    # 4. Invoke the notification microservice
    print('\n\n-----Invoking notification microservice-----')
    notification_result = invoke_http(
        "http://localhost:5008/notification", method="POST", json=delivery_result['data'])
    print("notification_result:", notification_result, '\n')

    # Check the notification result;
    # if a failure, send it to the error microservice.
    code = notification_result["code"]
    if code not in range(200, 300):

    # Inform the error microservice
        print('\n\n-----Invoking error microservice as notification fails-----')
        invoke_http("http:localhost:5007/error", method="POST", json=notification_result)
        print("Notification status ({:d}) sent to the error microservice:".format(
            code), notification_result)

    # 7. Return error
        return {
            "code": 400,
            "data": {
                "delivery_result": delivery_result,
                "Notification_result": notification_result
            },
            "message": "Error when sending notification to driver/customer."
        }

    # 7. Return updated delivery, notification status 
    return {
        "code": 201,
        "data": {
            "order_result": delivery_result,
            "notification_result": notification_result
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
