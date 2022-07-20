import keys
from telebot.async_telebot import AsyncTeleBot
import flight_finder as ff
import asyncio
from pprint import pprint
import json

TOKEN = keys.telegram_api
bot = AsyncTeleBot(TOKEN, parse_mode=None)
flight = ff.FlightHandler()


@bot.message_handler(commands=['start'])
async def start(message):
    await bot.reply_to(message, f"CIAO RAGAZZI!!\n"
                          f"Welcome to the Hasmer Flight tracker. {message.from_user.first_name}"
                          f"\nYou can type /help to see what you can do!")


@bot.message_handler(commands=['help'])
async def helper(message):
    help_msg = """
    First of all: type in '/ciao'
    /europe: Gets top 3 best cost/performance choices from ESB to various europe countries for you to travel!
    /iata: Gets iata codes for various regions, airports, cities etc. (not working yet)
    """
    await bot.reply_to(message, help_msg)


@bot.message_handler(commands=['ciao'])
async def send_welcome(message):
    await bot.reply_to(message, f"CIAO RAGAZZI!!")


@bot.message_handler(commands=['europe'])
async def europe_command_handler(message):
    parameters = message.text.split(" ")[1:]
    length = len(message.text.split(" "))
    if length == 1:
        await get_eur_flights(message)
    elif any(["=" not in bo for bo in parameters]):
        await bot.reply_to(message, "Incorrect syntax. Please check /europehelp")
    else:
        await bot.reply_to(message, "We're working on modified searches")
        pprint(parameters)


async def get_eur_flights(message):
    print(len(message.text.split(" ")))
    eur_flights = flight.search_flight_eur()
    fx_rate = f"Current FX rate is: {float(eur_flights['fx_rate']):.2f}"
    await bot.reply_to(message, fx_rate)
    for each in ff.display_results(eur_flights):
        await bot.reply_to(message, each)
    print(message.text)
    print(message.chat)


@bot.message_handler(commands=['iata'])
async def iata_handler(message):
    pass


@bot.message_handler(commands=["europehelp"])
async def europe_help(message):
    await bot.reply_to(message, "We're still working on modified searches")

# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     print(message)
#     print(vars(message))
#     print(f"text: {message.text}")
#     print(len(message.text))
#     bot.reply_to(message, f"You said {message.text}")


asyncio.run(bot.infinity_polling())
