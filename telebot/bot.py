import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from credentials import TOKEN, USERNAME, URL
import requests
import json

from invokes import invoke_http
from os import environ

#serviceURLs for simple microservices
driver_URL = environ.get('driverURL') or 'http://127.0.0.1:5001/driver'
customer_URL = environ.get('customerURL') or 'http://127.0.0.1:5002/customer'

#initialise global variables
global chat_ID
global account_type

def start(update, context):
    message = "Hello there! Reply 'Register as Customer' or 'Register as Driver' for timely Cheetah Express delivery notifications through this channel!! :)" 
    # message = "Congratulations! Thank you for registering your telegram with Cheetah Express. You can look forward to timely updates of your deliveries through this channel."
    update.message.reply_text(message)


def verify_intent(update, context):
    global chat_ID
    global account_type

    chat_ID = update.message.chat_id
    response = update.message.text
    response_tele_ID = update.message.chat.username

    if "register" in response.lower() and "customer" in response.lower():
        account_type = "customer"
        verification = update_customer_chatID(response_tele_ID)
        if verification == True:
            message = "Thank you! Reply 'confirm' to confirm your registration."
            update.message.reply_text(message)
        else:
            message = verification
            update.message.reply_text(message)
    elif "register" in response.lower() and "driver" in response.lower():
        account_type = "driver"
        verification = update_driver_chatID(response_tele_ID)
        if verification == True:
            message = "Thank you! Reply 'confirm' to confirm your registration."
            update.message.reply_text(message)
        else:
            message = verification
            update.message.reply_text(message)
    elif "confirm" in response.lower():
        message = "Congratulations, registration is successfull! Thank you for registering your telegram with Cheetah Express. You can look forward to timely updates of your deliveries through this channel."
        update.message.reply_text(message)
    else:
        message = "You can register with us anytime! :)"
        update.message.reply_text(message)


def update_customer_chatID(response_tele_ID):
    #invoke update customer using tele_ID
    customer_json = {
        "tele_chat_ID": chat_ID
    }
    #customer_data is a Python dict
    customer_data = invoke_http(customer_URL + '/' + str(response_tele_ID), method='PUT', json=customer_json)
    #verify db response
    # print(customer_data)
    code = customer_data['code']
    if code == 202:
        message = True
    elif code == 400:
        message = "Seems like you have already registered with us! Thank you ~"
    elif code == 404:
        message = "Seems like you do not have an account! Do create an account first :)"
    else: #code == 500
        message = "Registration is unsuccessful! Please try again."
    return message

def update_driver_chatID(response_tele_ID):
    #invoke update driver using tele_ID
    driver_json = {
        "tele_chat_ID": chat_ID
    }
    #driver_data is a Python dict
    driver_data = invoke_http(driver_URL + '/' + str(response_tele_ID), method='PUT', json=driver_json)
    #verify db response
    print(driver_data)
    code = driver_data['code']
    if code == 202:
        message = True
    elif code == 400:
        message = "Seems like you have already registered with us! Thank you ~"
    elif code == 404:
        message = "Seems like you do not have an account! Do create an account first :)"
    else: #code == 500
        message = "Registration is unsuccessful! Please try again."
    return message


def main():
    global bot
    global updater
    bot = telegram.Bot(token=TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher =  updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, verify_intent))

    updater.start_polling()

if __name__  == "__main__":
    main()
