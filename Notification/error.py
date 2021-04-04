#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
from flask import Flask, request, jsonify
import json
import os

import amqp_setup
import telegram_send
from invokes import invoke_http

monitorBindingKey='*.error'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'Error'
    
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
    invoke_http('https://api.telegram.org/bot1771827825:AAHVkbX5b9YpUWE78cTcBjz0SwkHqhrPbFA/sendMessage?chat_id=230470702&text=hello', method='GET')
    # telegram_send.send(messages=[message])


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()