#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import keys
import pprint
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging
import flight_finder as ff
from pprint import pprint

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
flight = ff.FlightHandler()


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    print(update.message.text)
    reply = f"""CIAO RAGAZZI !!
Welcome to the Hasmer Flight Tracker, {user.first_name}. 
Type in /help to see what you can do with the bot."""
    await update.message.reply_html(
        reply,
    )
    # await update.message.reply_html(
    #     reply_text,
    #     reply_markup=ForceReply(selective=True),
    # )


async def ciao(update, context):
    await update.message.reply_text("CIAO RAGAZZI !!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_msg = """
        First of all: type in '/ciao'
        /europe: Gets top 3 best cost/performance choices from ESB to various europe countries for you to travel!
        /iata: Gets iata codes for various regions, airports, cities etc. (not working yet)
        """
    await update.message.reply_text(help_msg)


async def europe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    parameters = update.message.text.split(" ")[1:]
    pprint(parameters)
    print(parameters)
    length = len(update.message.text.split(" "))
    if length == 1:
        await get_eur_flights(update, context)
    elif any(["=" not in bo for bo in parameters]):
        await update.message.reply_text("Incorrect syntax. Please check /europehelp")
    else:
        await update.message.reply_text("We're working on modified searches")


async def get_eur_flights(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    eur_flights = flight.search_flight_eur()
    fx_rate = f"Current FX rate is: {float(eur_flights['fx_rate']):.2f}"
    await update.message.reply_text(fx_rate)
    for each in ff.display_results(eur_flights):
        await update.message.reply_html(each)


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Echo the user message."""
#     await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(keys.ptb_api).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("europe", europe))
    application.add_handler(CommandHandler("ciao", ciao))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
