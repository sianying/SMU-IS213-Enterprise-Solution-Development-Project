# import requests
# import json
# import telegram

# from credentials import TOKEN, USERNAME, url

# global bot
# bot = telegram.Bot(token=TOKEN)

# def get_url(url):
#     response = requests.get(url)
#     content = response.content.decode("utf-8")
#     return content

# def main():
#     while True:
#         updates = get_url(url + "getUpdates?timeout=100")
#         print(updates)


# if __name__ == '__main__':
#     main()


from flask import Flask, request
from flask_cors import CORS
import telegram
# from telebot.credentials import TOKEN, USERNAME, URL
# from telebot.mastermind import get_response

HOST = "0.0.0.0"
PORT = 5006

TOKEN = "1672787508:AAF_XDgmu6-xl0YWsrFzTL4i6Jw5fBNymqo"
USERNAME = "Testing_jww_bot"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

global bot
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
CORS(app)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    tele_ID = update.message.chat.username

    print(chat_id)
    print(tele_ID)

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    # response = get_response(text)
    response = "Thank you for registering with Cheetah Express for the Telegram Notifications! /nThis method of Notification is as fast as Cheetah Express!"
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    set_up = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if set_up:
        return "Webhook setup is successful"
    else:
        return "Webhook setup has failed"

@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    print("Telegram webhook is ready.. " + "/n Running at PORT: "+ str(PORT) + ", HOST: " + HOST)
    app.run(host=HOST, port=PORT, threaded=True)