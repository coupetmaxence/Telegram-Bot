#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Note : Bot Telegram fournissant des informations sur la blockchain du bitcoin
    Modifié à partir de l'exemple echobot2.py fournit avec la documentation sur github
"""

"""
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
TOKEN = "Your token here"

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import logging
import requests
from emoji import emojize

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CURRENCY, VALUE = range(2)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi, I\'m the bitcoin bot! '+ emojize(":wave:", use_aliases=True)+
                              "\nCheck the command /help to know what I can do for you.")


def help(bot, update):
    update.message.reply_text('This Telegram bot provides informations about bitcoin\'s blockchain.\n\n'+
                              emojize(":small_blue_diamond:", use_aliases=True)+' /balance : Returns the final balance in bitcoin of the address '
                              'given in parameter.\n\n'+emojize(":small_blue_diamond:", use_aliases=True)+ ' /historic : Returns the 5 last transactions'
                              +' of the address given in parameter.\n\n'+emojize(":small_blue_diamond:", use_aliases=True)+' /ticker : Returns the value '
                              +'of 1 bitcoin in different currencies.\n\n'+emojize(":small_blue_diamond:", use_aliases=True)+' /convert : Begins a '
                              +'conversation with the user and lead to the converion from bitcoin to other currencies or from other currencies to bitcoin.'
                              +'\n\n'+emojize(":small_blue_diamond:", use_aliases=True)+' /cancel : Allow you to cancel the process of conversion.')


def echo(bot, update):
    update.message.reply_text("Sorry, but I did'nt understood your query.\nPlease check the command /help to know what I can do for you.")

def balance(bot, update):
    text = update.message.text
    text = text[8:] # on enlève la commande
    if(len(text)>0):
        while(text[0]==" " or text[0]=="," or text[0]==":"):
            text = text[1:]
        # on enlève tout caractere en trop
        if(text.isalnum() and len(text)==34): # on teste que l'entree est bien une adresse valide
            r = requests.get(url='https://api.blockcypher.com/v1/btc/main/addrs/'+text+'/balance')
            js = r.json()
            valeur_btc = float(js['final_balance'])/100000000
            moneybag = emojize(":small_blue_diamond:", use_aliases=True)
            update.message.reply_text("Balance of address " + text +" :\n\n"+moneybag+" "+ str(round(valeur_btc,5))+" BTC")
        else:
            update.message.reply_text("Invalid address, please try again.")
    else:
        update.message.reply_text("You must provide an address besides this command.")

        

def historic(bot, update):
    text = update.message.text
    text = text[9:] # on enlève la commande
    if(len(text)>0):
        while(text[0]==" " or text[0]=="," or text[0]==":"):
            text = text[1:]
        # on enlève tout caractere en trop
        if(text.isalnum() and len(text)==34): # on teste que l'entree est bien une adresse valide
            r = requests.get(url='https://api.blockcypher.com/v1/btc/main/addrs/'+text)
            js = r.json()
            txs = js['txrefs']
            valeur_btc = float(js['final_balance'])/100000000
            moneybag = emojize(":small_blue_diamond:", use_aliases=True)
            strMessage = "5 last transactions of address " + text +" :\n\n"
            for i in range(0,5):
                strMessage += moneybag +" Type : "
                if(txs[i]["tx_input_n"] < 0):
                    strMessage += "output"
                else:
                    strMessage += "input"
                strMessage += "\n      Value : "+str(txs[i]["value"]/100000000)+" BTC\n\n"
            update.message.reply_text(strMessage)
        else:
            update.message.reply_text("Adresse invalide, veuillez réessayer.")
    else:
        update.message.reply_text("You must provide an address besides this command.")

def ticker(bot, update):
    text = update.message.text
    text = text[7:] # on enlève la commande
    tickers = {"USD","GBP","EUR","JPY","CAD","HKD"}
    if(len(text)>0):
        print("zeze")
    else:
        r = requests.get(url='https://blockchain.info/fr/ticker')
        js = r.json()
        strMessage = "Value of 1 BTC in the currency.\n\n"
        index = emojize(":small_blue_diamond:", use_aliases=True)
        for tick in tickers:
            strMessage += index+" "+tick+" : "+str(js[tick]["last"])+"\n"
        update.message.reply_text(strMessage)

def convert(bot, update):
    reply_keyboard = [['BTC to USD', 'BTC to GBP', 'BTC to EUR','BTC to JPY'],['BTC to CAD', 'BTC to HKD', 'USD to BTC','GBP to BTC'],
                      ['EUR to BTC', 'JPY to BTC', 'CAD to BTC','HKD to BTC']]
    update.message.reply_text('Wich conversion would you like to make ?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CURRENCY

first = ""
second = ""

def currency(bot, update):
    global first, second
    tickers = {"USD","GBP","EUR","JPY","CAD","HKD"}
    text = update.message.text
    first = text[0:3]
    if(first == "BTC"):
        second = text[7:10]
        if(second in tickers):
            update.message.reply_text("Conversion from "+first+" to "+second+" :\nChoose a value to convert.",reply_markup=ReplyKeyboardRemove())
            return VALUE
        else:
            update.message.reply_text("Incorrect input, try again.")
            return CURRENCY
    else:
        if(first in tickers):
            second = text[7:10]
            if(second == "BTC"):
                update.message.reply_text("Conversion from "+first+" to "+second+" :\nChoose a value to convert.",reply_markup=ReplyKeyboardRemove())
                return VALUE
            else:
               update.message.reply_text("Incorrect input, try again.")
               return CURRENCY
        else:
            update.message.reply_text("Incorrect input, try again.")
            return CURRENCY

def value(bot, update):
    text = update.message.text
    valeur = 0.0
    try:
        valeur = float(text)
    except ValueError:
        update.message.reply_text("Incorrect value, try again.")
        return VALUE
    r = requests.get(url='https://blockchain.info/fr/ticker')
    js = r.json()
    if(first == "BTC"):
        js = js[second]
        update.message.reply_text(str(valeur)+" BTC = "+str(valeur*float(js['last']))+" "+second)
        return ConversationHandler.END
    else:
        js = js[first]
        update.message.reply_text(str(valeur)+" "+first+" = "+str(valeur/float(js['last']))+" BTC")
        return ConversationHandler.END

def cancel(bot, update):
    update.message.reply_text('Conversion cancelled.',reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # conv handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('convert', convert)],
        states={
            CURRENCY: [MessageHandler(Filters.text, currency)],
            VALUE: [MessageHandler(Filters.text, value)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("historic", historic))
    dp.add_handler(CommandHandler("ticker", ticker))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
