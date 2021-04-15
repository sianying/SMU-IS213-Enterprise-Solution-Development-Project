import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from credentials import TOKEN, USERNAME, URL
import requests
import json
import sqlalchemy as db
from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table

from os import environ

#db connection for customer and driver
customer_dbURL = environ.get('dbURL') or 'mysql+mysqlconnector://root@127.0.0.1:3306/customer'
driver_dbURL = environ.get('dbURL') or 'mysql+mysqlconnector://root@127.0.0.1:3306/driver'

#create the db model for customer
c_engine = create_engine(customer_dbURL, pool_recycle=3600)
c_metadata = MetaData()
customer = Table(
    "customer", c_metadata,
    Column("customer_ID", Integer, primary_key=True),
    Column('customer_name', String(64)),
    Column('customer_email', String(128)),
    Column('customer_mobile', Integer),
    Column('customer_teleID', String(20)),
    Column('tele_chat_ID', String(20))
)

#create the db model for the driver
d_engine = create_engine(driver_dbURL, pool_recycle=3600)
d_metadata = MetaData()
driver = Table(
    "driver", d_metadata,
    Column("driver_ID", Integer, primary_key=True),
    Column('driver_name', String(64)),
    Column('driver_email', String(128)),
    Column('driver_mobile', Integer),
    Column('vehicle_no', String(8)),
    Column('driver_teleID', String(20)),
    Column('tele_chat_ID', String(20))
)

#initialise their db engines
c_metadata.create_all(c_engine)
d_metadata.create_all(d_engine)

global chat_ID
global account_type

def start(update, context):
    message = "Hello there! Reply 'Register as Customer' or 'Register as Driver' for timely Cheetah Express delivery notifications through this channel!! :)" 
    update.message.reply_text(message)


def verify_intent(update, context):
    global chat_ID
    global account_type
    chat_ID = update.message.chat_id
    response = update.message.text
    if "register" in response.lower() and "customer" in response.lower():
        account_type = "customer"
        verification = verify_customer_chatID()
        if verification == True:
            message = "Thank you! Reply 'confirm' to confirm your registration."
            update.message.reply_text(message)
        else:
            message = verification
            update.message.reply_text(message)
    elif "register" in response.lower() and "driver" in response.lower():
        account_type = "driver"
        verification = verify_driver_chatID()
        if verification == True:
            message = "Thank you! Reply 'confirm' to confirm your registration."
            update.message.reply_text(message)
        else:
            message = verification
            update.message.reply_text(message)
    elif "confirm" in response.lower():
        response_tele_ID = update.message.chat.username
        if account_type == "customer":
            registration = update_customer_chatID(response_tele_ID)
            message = registration
            update.message.reply_text(message)
        elif account_type == "driver":
            registration = update_driver_chatID(response_tele_ID)
            message = registration
            update.message.reply_text(message)
    else:
        message = "You can register with us anytime! :)"
        update.message.reply_text(message)


def verify_customer_chatID():
    query = customer.select().where(customer.c.tele_chat_ID == chat_ID)
    conn = c_engine.connect()
    result = conn.execute(query)
    row = result.fetchall()
    if len(row) == 0:
        message = True
    else:
        message = "Seems like you have already registered with us! Thank you ~"
    return message

def verify_driver_chatID():
    query = driver.select().where(driver.c.tele_chat_ID == chat_ID)
    conn = d_engine.connect()
    result = conn.execute(query)
    row = result.fetchall()
    if len(row) == 0:
        message = True
    else:
        message = "Seems like you have already registered with us! Thank you ~"
    return message

def update_customer_chatID(response_tele_ID):
    update = customer.update().where(customer.c.customer_teleID == response_tele_ID).values(tele_chat_ID = chat_ID)
    conn = c_engine.connect()
    result = conn.execute(update)

    query = customer.select().where(customer.c.tele_chat_ID == chat_ID)
    conn = c_engine.connect()
    result = conn.execute(query)
    row = result.fetchall()
    if len(row) != 0:
        message = "Congratulations, registration is successfull! Thank you for registering your telegram with Cheetah Express. You can look forward to timely updates of your deliveries through this channel."
    else:
        message = "Registration is unsuccessful! Please try again."
    return message

def update_driver_chatID(response_tele_ID):
    update = driver.update().where(driver.c.driver_teleID == response_tele_ID).values(tele_chat_ID = chat_ID)
    conn = d_engine.connect()
    result = conn.execute(update)

    query = driver.select().where(driver.c.tele_chat_ID == chat_ID)
    conn = d_engine.connect()
    result = conn.execute(query)
    row = result.fetchall()
    if len(row) != 0:
        message = "Congratulations, registration is successfull! Thank you for registering your telegram with Cheetah Express. You can look forward to timely updates of your deliveries through this channel."
    else:
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
