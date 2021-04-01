#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os

import amqp_setup
import telegram_send

monitorBindingKey='customer.#'


def orderCreationSuccess():
    amqp_setup.check_setup()
        
    queue_name = 'Customer_Notification'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    message = json.loads(body)
    processOrderLog(json.loads(body))
    send_telemessage(message)

def processOrderLog(order):
    # print("Recording an order log:")
    print(order)

def send_telemessage(message):
    print("sending telegram message")
    telegram_send.send(messages=["hello"])


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    orderCreationSuccess()