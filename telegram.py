import keys
import telebot
from pprint import pprint
import json

TOKEN = keys.telegram_api
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# class TelegramBotHandler:
#     def __init__(self, token):
#         self.base_url = f"https://api.telegram.org/bot{token}"


@bot.message_handler(commands=['ciao'])
def send_welcome(message):

    print(message.text)
    print(message.chat)
    print(type(message.chat.id))
    print(message.chat.first_name)
    bot.reply_to(message, f"ciao ragazzi!!! {message.chat.first_name}")


@bot.message_handler(commands=['europe'])
def get_eur_flights(message):
    bot.reply_to(message, "ciao ragazzi!!!")
    print(message.text)
    print(message.chat)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"ciao ragazzi!! {message.text}")


bot.infinity_polling()
